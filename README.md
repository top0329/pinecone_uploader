# ディレクトリ構成
- **pdf**
  - **docs**: PineconeにアップロードするPDFファイルが集められるフォルダ
  - **app.py**: PDFファイルを処理するスクリプト
  - **pdf_urls.py**: URLで定義されたPDFの配列を持つファイル
- **html**
  - **kintone-sol.py**: `https://kintone-sol.cybozu.co.jp/integrate/search/name/` の各ガイド内容をPineconeに登録するスクリプト

# スクリプトの実行方法

## 必要なライブラリのインストール

以下のコマンドを実行して、必要なライブラリをインストールしてください:

```bash
pip install -r requirements.txt
```

## スクリプトの実行

以下のコマンドでスクリプトを実行します:

```bash
python app.py
python kintone-sol.py
```

## `pdf` ディレクトリの説明
このスクリプトを実行すると、`pdf_urls.py` に記載されたPDFファイルが `docs` フォルダにダウンロードされます。その後、`docs` フォルダ内にあるすべてのPDFファイルが、Pineconeベクターデータベースにアップロードされます。

## `html` ディレクトリの説明
このスクリプトを実行すると、`https://kintone-sol.cybozu.co.jp/integrate/search/name/` にある各ガイドの内容が抽出され、Pineconeに登録されます。