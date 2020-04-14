LC Manager
==========

A simple GUI application for managing HPLC data.

![Python version][shield-python]
![openpyxl version][shield-openpyxl]
![PySimpleGUI version][shield-pysimplegui]
![Licence][shield-license]

Overview
-----------------

* Edit HPLC data. (e.g. "calculate RRT", "exclude unnecessary peak")
* Create a table like below which has columns(rrt, samples) from multiple HPLC data.
* Export the edited data and the table as xlsx(Excel) file.

You can see the percentage of specific impurities in each sample.

| RRT    | sample1 | sample2 | sample3 |
| :----: | :-----: | :-----: | :-----: |
| 0.5    | 95.50%  | 85.40%  | 65.30%  |
| 1.0    | 3.50%   | 13.50%  | 33.50%  |
| 1.5    | 1.00%   | 1.10%   | 1.20%   |

Table of Contents
-----------------

* [Requirements](#requirements)
* [Usage](#usage)
* [License](#license)


Requirements
------------

LC Manager requires the following to run:

* [Python][python] 3.7
* [openpyxl][openpyxl] 3.0.3
* [PySimpleGUI][pysimplegui] 4.16.0


Usage
-----
When you start the application, the following screen will be displayed

<img width="615" alt="スクリーンショット 2020-04-14 22 05 20" src="https://user-images.githubusercontent.com/52167040/79228809-065dd780-7e9d-11ea-9db7-548e13804afa.png">


### Input HPLC data
First, import the HPLC data that you want to edit.  
There are two ways of importing data

1.Use the ASCII files output from the HPLC system  
Outputs HPLC data from the HPLC system in ASCII format.
Press the "Input ASCII" button to select multiple ASCII files from the popup and press the "Browse" button and press "OK"

<img width="614" alt="スクリーンショット 2020-04-14 22 25 59" src="https://user-images.githubusercontent.com/52167040/79230027-f8a95180-7e9e-11ea-8916-ab8cd4283ddb.png">



2.Use the text in the original format as described below  
Press the "Input Text" button to select a text file from the pop-up and press the "Browse" button and press "OK".

### preparation text data
Before using this application, please prepare a text file(.txt) based on your HPLC data in the following format.
It can be easily prepared by copying from the HPLC system (s.g. "Shimazu", "Waters", "Agilent")  
sample.txt is in repository.

---
//Format//  
\#sample name (**Name MUST start with "#"**)  
RT  Area    Ratio (tab delimited)  
RT  Area    Ratio  
RT  Area    Ratio  

\#next sample name  
RT  Area    Ratio  
RT  Area    Ratio  

repeat for all your analysis data  
(Note: RT means retention time)

---

---
//Example//  
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

### calculate RRT
If you want calculate relative retention time, press "Calc RRT" button on the Edit frame.
Then fill out base RT for calculating RRT in the popup window.  
Note: If there is the RT between base RT-0.2 and +0.2 in analysis sample, RRT is calculated by the RT.
If not, RRT is calculated by base RT.  
<img width="612" alt="スクリーンショット 2020-04-14 22 08 58" src="https://user-images.githubusercontent.com/52167040/79230335-62c1f680-7e9f-11ea-9ca6-48bf2880db0b.png">
<img width="615" alt="スクリーンショット 2020-04-14 22 31 27" src="https://user-images.githubusercontent.com/52167040/79230539-b6344480-7e9f-11ea-83fa-868fc30dba89.png">


### name peaks
Perhaps you know what the peak with the certain RRT. You can name peaks by pressing "Set Peak Names" button.  
In the popup window that appears, fill out names for each RRT (You do not need to fill in all).  
<img width="624" alt="スクリーンショット 2020-04-14 22 09 35" src="https://user-images.githubusercontent.com/52167040/79230604-d2d07c80-7e9f-11ea-9df5-cfc5f1252443.png">


### exclude unnecessary peaks
If you want to exclude certain peaks(s.g. blank peaks, solvent peaks) when calculating the area ratio,
click the "Exclude" button. Then enter the each name of the peaks you want to exclude in the popup window that appears,

Note: You should name peaks before excluding peaks.

<img width="612" alt="スクリーンショット 2020-04-14 22 10 31" src="https://user-images.githubusercontent.com/52167040/79230673-ee3b8780-7e9f-11ea-8ae8-d88911d90f45.png">
<img width="613" alt="スクリーンショット 2020-04-14 22 10 49" src="https://user-images.githubusercontent.com/52167040/79230735-027f8480-7ea0-11ea-87c9-8444f1038255.png">


### export xlsx
After editing your data, press the "Export Excell File" button to save xlsx file.




### Contact Infomation
mail: humi20190106@gmail.com
twitter:@IT_parsely
Github: parsely1231



License
-------

LC Manager is licensed under the MIT license.
Copyright &copy; 2020, parsely



[shield-coverage]: https://img.shields.io/badge/coverage-100%25-brightgreen.svg
[shield-dependencies]: https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg
[shield-license]: https://img.shields.io/badge/license-MIT-blue.svg
[shield-python]: https://img.shields.io/badge/python-v3.7-blue
[shield-openpyxl]: https://img.shields.io/badge/openpyxl-v3.0.3-blue.svg
[shield-pysimplegui]: https://img.shields.io/badge/pysimplegui-v4.16.0-blue.svg
[shield-build]: https://img.shields.io/badge/build-passing-brightgreen.svg
[python]: https://www.python.org/
[openpyxl]: https://openpyxl.readthedocs.io/en/stable/index.html
[pysimplegui]: https://pysimplegui.readthedocs.io/en/latest/