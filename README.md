# README

## **フォルダ構成**

フォルダ構成は以下のようになっている。

```jsx
└── code
     ├──Results
     │     ├──result1.txt
     │     ├──result2.txt
     │     ├──result3.txt
     │     └──result4.txt
     ├──TestCase
     │     ├──create_testcase.py
     │     ├──test.txt
     │     ├──test1.txt
     │     ├──test2.txt
     │     ├──test3.txt
     │     └──test4.txt
     ├──Q1.py
     ├──Q2.py
     ├──Q3.py
     └──Q4.py
```

各課題の監視ログデータ

```jsx
code/TestCase
```

各課題の出力結果

```jsx
code/Results
```

## **使い方**

初めに以下のコマンドでgithubからソースコードをダンロードする。

```jsx
git clone https://github.com/Ryuta44/CodingTest.git
```

次にディレクトリを移動する。

```
cd CodingTest
```

### 課題の実行方法

課題1

```jsx
python3 code/Q1.py
```

以降の課題も"Qx.py"のxを課題に対応する番号を入れて実行する。

またコードの解説は"Qx.txt"に記載されている。

## **実行結果**

課題1

```jsx
IPアドレス:10.20.30.1/16
failure : 2020年10月19日 13:32:24 - 2020年10月19日 13:35:24
failure : 2020年10月19日 13:41:24 -      ----------

IPアドレス:10.20.30.2/16
failure : 2020年10月19日 13:34:25 - 2020年10月19日 13:35:25
failure : 2020年10月19日 13:38:25 - 2020年10月19日 13:39:25

IPアドレス:192.168.1.1/24
failure : 2020年10月19日 13:33:34 - 2020年10月19日 13:35:34
failure : 2020年10月19日 13:36:34 - 2020年10月19日 13:37:34

IPアドレス:192.168.1.2/24
failure : 2020年10月19日 13:41:35 -      ----------
```

課題2

```jsx
IPアドレス:10.20.30.1/16
failure : 2020年10月19日 13:33:24 - 2020年10月19日 13:36:24
failure : 2020年10月19日 13:38:24 -      ----------

IPアドレス:10.20.30.2/16
failure : 2020年10月19日 13:32:25 - 2020年10月19日 13:36:25

IPアドレス:192.168.1.2/24
failure : 2020年10月19日 13:41:35 -      ----------
```

課題3

```jsx
IPアドレス:192.168.1.1/24
overload : 2020年10月19日 13:37:34 - 2020年10月19日 13:39:34
overload : 2020年10月19日 13:37:34 - 2020年10月19日 13:39:34

IPアドレス:192.168.1.2/24
overload : 2020年10月19日 13:37:35 - 2020年10月19日 13:39:35
overload : 2020年10月19日 13:37:35 - 2020年10月19日 13:39:35
failure  : 2020年10月19日 13:40:35 -      ----------

IPアドレス:10.20.30.2/16
overload : 2020年10月19日 13:38:25 - 2020年10月19日 13:41:25
```

課題4

```jsx
サブネットアドレス:10.20.0.0
failure : 2020年10月19日 13:32:24 - 2020年10月19日 13:35:24

サブネットアドレス:192.0.0.0
failure : 2020年10月19日 13:35:34 - 2020年10月19日 13:37:34
failure : 2020年10月19日 13:41:34 -      ----------
```
