# Registro de validação

Pedro Artur Brandão Murillo e Daniel de Oliveira Teixeira Silva. Unilasalle-RJ,
Sistemas de Informação, Linguagem de Programação, 6º período, 2026.

## Ambiente e escopo

Validação local em 11/11/2026, Windows, Python 3.14.7, ambiente virtual exclusivo.
Versões estritas em `requirements.txt`; `pip check` sem conflitos.

## Evidências executadas

- Arquivo bruto preservado; SHA-256 verificado contra a proveniência.
- MD5 do XLSX conferido contra o manifesto interno.
- Base lida: 14.517 registros município/rede e 133 colunas.
- Recorte: 92 códigos municipais distintos, rede Municipal, RJ.
- Normalização: 1.012 linhas, 998 Idebs válidos, 14 ausentes; nenhuma imputação.
- Cobertura recalculada e compatível com a inspeção inicial da coleta.
- 998 combinações Ideb/P/N dentro da tolerância de arredondamento de 0,0501.
- Oito testes automatizados do pipeline aprovados.
- Notebook inteiro executado sem erro por `scripts/execute_notebook.py`.
- Reexecução do pipeline com hashes idênticos para os produtos registrados
  em `reproducibilidade.json` (dados, tabelas, métricas, artigo e figuras).
- Resumo do artigo com 198 palavras; quatro figuras com texto alternativo;
  referências a arquivos locais e âncoras válidas.
- JavaScript verificado com `node --check docs/assets/app.js`.
- Artigo servido localmente com resposta HTTP 200.
- Quatro figuras estáticas inspecionadas visualmente a partir de renderizações
  PNG de conferência; eixos, legendas e rótulos legíveis.

## Limites e pendências explícitas

- Comparação dos bytes da entrada com o download direto do Inep: pendente.
  Integridade interna e origem declarada não comprovam autenticidade independente.
- Licença específica dos dados: confirmação pendente; dados de terceiros não
  foram relicenciados. Código MIT, texto e figuras autorais CC BY 4.0.
- PDFs metodológicos complementares não integram a coleta; as notas internas
  da planilha foram preservadas.
- Verificação visual em navegador, em desktop e celular, não concluída: o host
  de acesso ao navegador está indisponível nesta sessão. CSS inclui regras
  responsivas e o conteúdo estático funciona sem JavaScript, mas isso não
  substitui a inspeção visual e o teste real dos controles Plotly.
- Ambiente diferente de Windows/Python 3.14: não homologado.
- O semestre letivo não foi informado; artefatos identificam 2026 e 6º período.

## Publicação

Repositório e pasta de publicação: `pedro-art2611/Projeto-Pr-ticoG2`, branch
`main`, `/docs`. Estado de deploy será atualizado após confirmação do GitHub.
