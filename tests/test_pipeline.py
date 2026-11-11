"""Contratos relevantes de integridade, ausência e comparação temporal."""
import hashlib
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from src.etl import ROOT, RAW_NAME, acquire, normalize, parse_numbers, read_source, write_csv
from src.analysis import analyze, correlations
from src.metadata import DERIVED_SCHEMAS


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = read_source(acquire(ROOT / "data/raw" / RAW_NAME))
        cls.data = normalize(cls.source)

    def test_decimal_and_missing_markers(self):
        result = parse_numbers(pd.Series(["5,9", "0", "-", "ND", "ND*", "ND***", ""]))
        self.assertEqual(result.iloc[0], 5.9)
        self.assertEqual(result.iloc[1], 0)
        self.assertTrue(result.iloc[2:].isna().all())

    def test_unknown_marker_is_not_silently_discarded(self):
        with self.assertRaisesRegex(ValueError, "não reconhecidos"):
            parse_numbers(pd.Series(["ERRO_INESPERADO"]))

    def test_tampered_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "corrompido.zip"
            path.write_bytes(b"entrada alterada")
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                acquire(path)

    def test_duplicate_municipality_is_rejected(self):
        row = self.source[(self.source.SG_UF == "RJ") & (self.source.REDE == "Municipal")].iloc[[0]]
        with self.assertRaisesRegex(ValueError, "92 municípios"):
            normalize(pd.concat([self.source, row], ignore_index=True))

    def test_population_keys_and_coverage(self):
        self.assertEqual(len(self.data), 1012)
        self.assertEqual(self.data.codigo_municipio.nunique(), 92)
        self.assertTrue(self.data.codigo_municipio.str.fullmatch(r"\d{7}").all())
        self.assertFalse(self.data.duplicated(["codigo_municipio", "rede", "etapa", "ano"]).any())
        expected = [88, 91, 91, 91, 91, 92, 89, 90, 91, 92, 92]
        self.assertEqual(self.data.groupby("ano").ideb.count().tolist(), expected)
        self.assertEqual(self.data.ideb.isna().sum(), 14)

    def test_missing_and_nonexistent_targets_preserved(self):
        missing = self.data[self.data.ideb.isna()]
        self.assertTrue(missing.ideb_original.eq("-").all())
        targets = self.data[self.data.ano.isin([2005, 2023, 2025])]
        self.assertTrue(targets.meta.isna().all())
        self.assertTrue(targets.meta_original.eq("").all())

    def test_paired_decomposition_and_rounding(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = analyze(self.data, Path(tmp))
        p = result["paired"]
        self.assertEqual(len(p), 92)
        self.assertEqual(result["metrics"]["painel_balanceado_n"], 82)
        np.testing.assert_allclose(p.contribuicao_rendimento + p.contribuicao_nota, p.delta_produto, atol=1e-12)
        self.assertTrue(p.residuo_arredondamento.abs().le(.1002).all())

    def test_gzip_is_independent_of_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a.csv.gz", Path(tmp) / "b.csv.gz"
            write_csv(a, self.data); write_csv(b, self.data)
            self.assertEqual(hashlib.sha256(a.read_bytes()).digest(), hashlib.sha256(b.read_bytes()).digest())
            restored = pd.read_csv(a, dtype={"codigo_municipio": str}, keep_default_na=False)
            self.assertEqual(len(restored), len(self.data))
            self.assertEqual(restored.ideb_original.eq("-").sum(), 14)

    def test_correlations_with_ties_and_missing_pair(self):
        # Postos de x: 1, 2.5, 2.5, 4; postos de y: 4, 2.5, 2.5, 1.
        data = pd.DataFrame({"ideb_2023": [1, 2, 2, 3, np.nan],
                             "ideb_2025": [8, 5, 5, 2, 9]})
        result = correlations(data)
        self.assertTrue(result.n_pares.eq(4).all())
        np.testing.assert_allclose(result.coeficiente, [-1, -1], atol=1e-12)

    def test_constant_series_has_no_defined_correlation(self):
        with self.assertRaisesRegex(ValueError, "variação"):
            correlations(pd.DataFrame({"ideb_2023": [1, 1, 1], "ideb_2025": [1, 2, 3]}))

    def test_every_derived_column_has_metadata(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            analyze(self.data, Path(tmp))
            for filename, schema in DERIVED_SCHEMAS.items():
                if filename == "validacao.json":
                    actual = json.loads((ROOT / "data/processed" / filename).read_text(encoding="utf-8"))
                elif filename.endswith(".json"):
                    actual = json.loads((Path(tmp) / "data/processed" / filename).read_text(encoding="utf-8"))
                else:
                    actual = pd.read_csv(Path(tmp) / "data/processed" / filename, nrows=0).columns
                self.assertEqual(set(actual), set(schema), filename)
                self.assertTrue(all(len(definition) == 3 and all(definition) for definition in schema.values()))


if __name__ == "__main__":
    unittest.main()
