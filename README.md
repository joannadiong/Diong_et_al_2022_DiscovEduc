# The effect of face-to-face versus online learning on student performance in anatomy: An observational study using a causal inference approach

Joanna Diong<sup>1</sup>, Hopin Lee<sup>2</sup>, Darren Reed<sup>1</sup>

1. School of Medical Sciences, Faculty of Medicine and Health, The University of Sydney
2. Nuffield Department of Orthopaedics, Rheumatology and Musculoskeletal Sciences, University of Oxford


## Suggested citation

Diong J, Lee H, Reed D (2022) The effect of face-to-face versus online learning on student performance in anatomy:
An observational study using a causal inference approach. Discover Education (in press).

## Protocol registration

Protocol registration on the Open Science Framework (OSF): [https://osf.io/ws8mv][rego]

OSF project repository: [https://osf.io/xhs83/][project]

## Data

De-identified processed data of examination marks for undergraduate and postgraduate cohorts are available in __data -> proc__:
* bios1168_proc_.csv
* bios5090_proc_.csv

De-identified raw data of introductory histology marks for the postgraduate unit are available in __data -> raw__:
* BIOS5090_histology.csv

## Code

Python (v3.9) and R (v4.2.2) code files were written by Joanna Diong.

### Python files

`script`: Main script to run analysis.

`proc`, `plot`, `utils`: Modules containing functions used to clean data and plot figures.

### Running Python code

A reliable way to reproduce the analysis would be to run the code in an
integrated development environment for Python (e.g. [PyCharm][pycharm]). 

Create a virtual environment and install dependencies.
Assuming you are running off Python on an [Anaconda distribution][Anaconda] or similar,
using the Terminal (Mac or Linux, or PyCharm Terminal), 

```bash 
python -m venv env
```
Next, activate the virtual environment. 

For Mac or Linux, 

```bash
source env/bin/activate
```

For Windows, 

```bash
.\env\Scripts\activate
```

Then, install dependencies,

```bash
pip install -r requirements.txt
```

Run `script.py`.

### R files

`script`: Main script to run analysis to obtain E-values.

### Running R code

Run `script.R`.

## Output

Python generated files, saved in __data -> proc__:
* bios1168_clean_.csv
* bios1168_result_.txt
* bios1168.pdf figure file
* bios5090_clean_.csv
* bios5090_result_.txt
* bios5090.pdf figure file

R generated file, saved in __data -> proc__:
* evalues.txt


[rego]: https://osf.io/ws8mv
[project]: https://osf.io/xhs83/
[spike2py]: https://github.com/MartinHeroux/spike2py
[Anaconda]: https://www.anaconda.com/products/distribution
[pycharm]: https://www.jetbrains.com/pycharm/promo/?gclid=Cj0KCQiAtqL-BRC0ARIsAF4K3WFahh-pzcvf6kmWnmuONEZxi544-Ty-UUqKa4EelnOxa5pAC9C4_d4aAisxEALw_wcB 
