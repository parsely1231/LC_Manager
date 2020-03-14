LC Manager
==========

HPLCのデータを編集・管理するためのGUIアプリケーションです。

![Python version][shield-python]
![openpyxl version][shield-openpyxl]
![PySimpleGUI version][shield-pysimplegui]
![Licence][shield-license]

概要
---

* HPLCデータを編集します. (e.g. RRT(相対保持時間)の計算, 不要なピークを計算から除外する)
* 複数の分析データから下表のようなテーブルを作成します.
* 編集したデータをエクセルファイルとして出力します.

それぞれの分析サンプルで各ピークがどのように推移しているかを容易に確認できます。

| RRT    | sample1 | sample2 | sample3 |
| :----: | :-----: | :-----: | :-----: |
| 0.5    | 95.50%  | 85.40%  | 65.30%  |
| 1.0    | 3.50%   | 13.50%  | 33.50%  |
| 1.5    | 1.00%   | 1.10%   | 1.20%   |

目次
-----------------

* [Requirements](README_en.md#requirements)
* [Usage](README_en.md#usage)
* [License](README_en.md#license)


必要な環境
---

アプリケーションを利用するために以下の環境が必要です。

* [Python][python] 3.7
* [openpyxl][openpyxl] 3.0.3
* [SimplePyGUI][simplepygui] 4.16.0


使用方法
---

### テキストの準備
編集したいHPLCデータを以下の様式でテキストファイルに変換する必要があります。
HPLCのシステムからコピーペーストすれば簡単に作成できると思います。 (s.g. "島津", "Waters", "Agilent")  
テキストサンプルがリポジトリの中にあるので参考にしてください。

---
//様式//  
\#sample name (**サンプルの名前の頭に"#"を入れてください**)  
RT  Area    Ratio (tab delimited)  
RT  Area    Ratio  
RT  Area    Ratio

\#next sample name  
RT  Area    Ratio  
RT  Area    Ratio

同様にして編集したい分析データを全て入力してください  
(Note: RTは保持時間のことです)

---

---
//例//  
\#sample_1  
1.222	10000	10.0  
2.222	10000	10.0  
9.123	80000	80.0

\#sample_2  
1.222	10000	10.0  
2.222	10000	10.0  
9.123	40000	40.0  
10.221	40000	40.0

---


### テキストファイルのInput
"Select File"ボタンを押してテキストファイルを選択し、"Input Data"ボタンを押してください。  
<img width="612" alt="スクリーンショット 2020-03-14 12 50 35" src="https://user-images.githubusercontent.com/52167040/76675660-1ca71800-65ff-11ea-8a97-eb688141e31f.png">



### RRTの計算
RRTを計算する場合、"Calc RRT"ボタンを押して、ポップアップにBase RTを入力してください。  
Note: サンプル内にBase RTの±0.2いないのRTがある場合、そのRTを基準としてRRTを計算します。該当するRTがない場合は、Base RTをつかってRRTを計算します。  
<img width="611" alt="スクリーンショット 2020-03-14 12 57 52" src="https://user-images.githubusercontent.com/52167040/76676395-4ca5e980-6606-11ea-964e-957323963f8a.png">  
<img width="611" alt="スクリーンショット 2020-03-14 12 58 10" src="https://user-images.githubusercontent.com/52167040/76676416-9262b200-6606-11ea-9fde-d0e55febb1c1.png">


### name peaks
特定のRRTに名前をつける場合、"Set Peak Names" ボタンを押してください.  
表示されたポップアップにRRT毎に設定した名前を入力してください (全てを埋める必要はありません。名前がない場合は空白で大丈夫です).  
<img width="611" alt="スクリーンショット 2020-03-14 12 58 28" src="https://user-images.githubusercontent.com/52167040/76676583-6811f400-6608-11ea-92f6-b69ceb293579.png">


### exclude unnecessary peaks
面積比を計算する際に、特定のピークを除去する場合(s.g. ブランクピーク, 溶媒ピーク)、"Set Exclude"ボタンを押してください。  
表示されたポップアップの中で計算から除外したいピーク名にチェックを入れてOKを押してください。
Note: この機能をしようする場合、先にピークに名前を設定する必要があります。  
<img width="612" alt="スクリーンショット 2020-03-14 12 58 53" src="https://user-images.githubusercontent.com/52167040/76676436-e077b580-6606-11ea-8eb0-4f3612d2fd2a.png">


### export xlsx
データの編集が終わったら、"Export Excel File"ボタンをおせば、xlsxファイルとして保存できます。



### Contact Infomation
使い方の質問や要望などありましたら気軽にご連絡ください。  
mail: humi20190106@gmail.com  
twitter:@IT_parsely  
Github: parsely1231


License
-------

LC Manager is licensed under the MIT license.  
Copyright &copy; 2020, parsely



[shield-license]: https://img.shields.io/badge/license-MIT-blue.svg
[shield-python]: https://img.shields.io/badge/python-v3.7-blue
[shield-openpyxl]: https://img.shields.io/badge/openpyxl-v3.0.3-blue.svg
[shield-pysimplegui]: https://img.shields.io/badge/pysimplegui-v4.16.0-blue.svg
[python]: https://www.python.org/
[openpyxl]: https://openpyxl.readthedocs.io/en/stable/index.html
[simplepygui]: https://pysimplegui.readthedocs.io/en/latest/