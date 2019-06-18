# *`solarpred`*

### A solar cycle predictor based on Machine Learning 

<!-- <img src=figures/solarpred.jpg alt="scythe-logo" style="position:absolute; height:95%; top:2.5% ; left:50%"/> -->

<br/>

## Table of contents
1. [Introduction](#intro)
1. [Findings](#findings)
    1. [First method:  linear dates and SVR](#m1)
    1. [Second method: linear dates and perceptron](#m2)
    1. [Third method:  linear dates without outliers and extra features with a linear regressor](#m3)
    1. [Fourth method:  linear dates without outliers and extra features with SVR](#m4)
    1. [Final method: cyclical dates without outliers with SVR](#m5)
1. [Method comparison matrix](#comparisonMatrix)
1. [Future lines of research](#futureResearch)
1. [User manual](#solarpred)
    1. [Installation](#installation)
    1. [Functionality](#functionality)
    1. [Options](#options)
1. [Future extensions of `solarpred`](#futureTODO)
1. [References](#references)
1. [Other recommended reading](#recommended)


<a name="intro"></a>
## Introduction 

This repository is intended as a container of all the findings encountered during the intership made by Miguel Jiménez Arribas in the department of Flight Dynamics and Operations (FDO) of GMV. The purpose of this intership was to investigate the inner workings of different machine learning (ML) techniques and how they could be used inside the department.

Following this objective, the tool named _`solarpred`_ was created. The main functionality of this program is to predict the evolution of the solar cycle using historical and recent data, providing as output the possible future values of the solar flux in the 10,7cm wavelength which can then be fed into the models of the simulations applied by FDO. During the investigation phase of this tool different alternatives were studied, which conclusions can be found in this document and on the Jupiter notebooks from the `notebooks/` repository. The source code of _`solarpred`_ can be found in `src/`, along with a JSON file containing a data estructure with all the employed data.

The rest of this document is divided in two main sections. First, a summary of the different machine learning techniques estudied during the project are presented, along with the results obtained and the conclusions that were arrived to. Secondly, the user manual of _`solarpred`_ is provided, explaining its functionality so that it could be integrated into the work process of the department.


<a name="findings"></a>
## Findings

One of the main findings during the internship was how important the data was for the machine learning algorithm to function properly. So much so, that changing the data formatting, adding extra features represented in different ways, etc., was as important as choosing the right estimator. For that reason, this section is divided in methods or approaches taken, each of them composed of a pair of data (with its features and internal format) and a ML algorithm. Ensuing, we will describe each one of them and how they performed predicting the evolution of the solar cycle, explaining the results found.

In this repository there is a folder called `notebooks/` where each of these approaches was tested on a Jupyter Notebook. Hence, the following explanations can be retested and played with to be fully understood using the code and descriptions found there. To be able to do this, it is neccesary to download and install Jupyter, for which the recommended steps are to install it using the Anaconda distribution, as most of the other tools needed for machine learning work will also be installed using this wrapper. 

To do this, you need to go to [this webpage](https://www.anaconda.com/distribution/#download-section) and download the version specificic for your system of Python 3. After it has finished downloading, you can execute the installer and follow the instructions given by it. Once Anaconda is installed you only need to search for Jupyter Notebook in the Anaconda software navigator (either in *"Home"* or in *"Environments"* and click on it to install it. After this is done, opening `Jupyter Notebook` from the Start menu on Windows will open a server in localhost from which all notebooks can be studied and executed.

<a name="m1"></a>
### First method: linear dates and SVR
After some time during which I got acquainted with the various tools used for the research and development of _`solarpred`_ (scikit-learn, Anaconda, etc.), the first approach taken to predict the solar cycle was extremely naive. 

In regards to the data, the SVR was fed with the downloaded historical record of the solar flux in the 10.7 Hz wavelength. These records were composed of a single feature, the date (from 1947 to 2019) formatted linearly and a single output goal, the mean 10.7 Hz solar flux of each day. What linearly formatted date means in this context will be made clear when we talk about cyclical features on the [last method](#m5), but basically it means that "2000 01 01" is followed by "2000 01 02" and this one is followed by "2000 01 03" and so forth, all along the temporal line instead of having a cyclical behaviour like a clock. This was later found to be a significant problem, as the estimators could not infer the cyclical nature of the data making unstisfactory predictions. 

Specifically in this first method, the data, which was downloaded in the format "YYYY MM DD", was translated with the Datetime python module to be an integer consisting on the number of days since January 1, of the year 0, following what is defined as the Proleptic Gregorian calendar. Hence, for example the 1st of January of 2000 is the number 730120.

With respect to the estimator, there were tests using both a support-vector machine (SVM) regressor [\(Scikit-learn developers, SVR\)](#svr1) and a Kernel Ridge Regressor. Unfortunately, all these tests were made on the same notebook (which can be found [here](/notebooks/SolarFlux_SVR_v1.ipynb "First method notebook")), and in the end, only the SVR solution can be seen in that link, though a comparison between both algorithms can be read on [\(Scikit-learn developers, KRR vs SVR\)](#krrsvr).

Other knowledge gained with this first method was the different ways to order the data for the cross-validation. For those uninitiated in Machine Learning or Statistics, cross-validation is the technique in which a data set is divided in three distinct segments. First, there is the training set which is used for the ML algorithm to be fitted to it, then there is the test set which is used to gather the performance of the generated model. When cross-validation is applied an extra set is created with the objective to test different parameters of the ML algorithm for overfitting, selection bias u other problems, so that the testing set can be reserved for only it purpose. Hence, during this first method is was found that KFold and the TimeSeriesSplit [\(Scikit-learn developers, KFold\)](#kfold) [\(Scikit-learn developers, TimeSeriesSplit\)](#tmsplit) were the more useful method of division to select which data point goes to which data set. In general, it was found that there should be used divisions without shuffling as this would defeat the time dependance of our data. 

Lastly, during this first method it was also learned about how data scaling can affect the training or fitting process, as if the data is not scaled outliers with big values can make the ML algorithm overfit the model; and about how different kernels influence the inner workings of the support-vector machine [\(Chih-Wei, H., Chih-Chung C., Chich-Jen, L., 2016\)](#svr2).


<a name="m2"></a>
### Second method:  linear dates and perceptron
Seeing that the performance of the previous method was not as suitable as expected, it was decided to try using neural networks to fit the data instead of SVMs. As the only neural network provided by the scikit-learn library was a perceptron, specifically a multilayer perceptron regresor [\(Scikit-learn developers, MLPRegressor \)](#mlpreg), that was the algorithm we used, which in retrospect, may not have been the best idea, as we suffered from the same problem as with the earlier method and the data fed to it was too poor to obtain any useful results.

As explained in the future lines of research [section](#futureResearch), having the data with no further treatment as it was at this moment in time, the only viable solution would have been using a recurrent neural network (RNN) to fit the data, as that would have, probably, deduced the cyclical nature of the data. Otherwise, the results were nearly identical to method number one. It should also be said that using the approach of data treatment described in the [final method](#m5) this algorithm could probably be used too with succesful results, instead of the SVM finally implemented, though this hasn't been tested.

The MLPRegressor solution and its results can be seen in this Jupyter [notebook](/notebooks/MLPRegressor.ipynb "Second method notebook").

<a name="m3"></a>
### Third method:  linear dates without outliers and extra features with multiple linear regressors
After having tested the most "powerful" ML algorithms without satisfactory results, it was time to focus the attention on exploring how the data format could influence the performance of the predictions. As such, it was dediced to start making some data treatment to the raw downloaded data.

First, we tried removing the outliers, especially the null values where no data was recorded and some of the first months high values, as they were abnormally high in comparison with the rest of the cycles. After this, we tried generating extra features by means of the `PolynomialFeatures` tool inside scikit-learn, which provides an easy way of creating polynomical features, that is, features based on the same data, e.g.: data set X, but polynomically increased, e.g.: X^2 , X^3, etc.

Once this was done we tried using a basic linear regressor to fit the data [\(Scikit-learn developers, Linear regression \)](#linreg), as now we had multiple dimensions in our data and so we could fit not only a linear but a quadratic or higher order model to the data. The full coded solution and its results can be seen in this [notebook](/notebooks/Polynomial_Linear_Regresion.ipynb "Third method notebook").

Still the results weren't satisfactory (even after scaling the polynomial features), so we increcreased the number of features, trying to display some kind of cyclical behaviour in the data, as it was suspected that the problem lied on the algorithms not being capable of infering the cyclical nature of the data on its own. With this objective there were added two extra features, the month and the year of each data point independently to the full date, so that even after converting to integer as explained earlier, it could be seen how the solar flux depended on the year and month it occurred. Still, the results weren't greatly improved. This method and its results can be seen coded [here](/notebooks/Polynomial_Linear_Regresion_month&year_features.ipynb "Third method notebook").

Finally, it should be said that in this notebook there were also tested different robust linear regressors, like the RANSAC, TheilSen or the Huber regressors, all of them with the same unsuccessful results. So in the end, only the last one mentioned can be seen on the previous link, though an article explaining their differences can be read on [\(Scikit-learn developers, Robust linear estimator fitting\)](#robustReg).

<a name="m4"></a>
### Fourth method:  linear dates without outliers and extra features with SVR
Thinking the approach of data treatment described in the previous method may be enough to obtain good results with a more complex ML algorithm, we tried to feed this data with all the different features (date, year, month, and the polynomial features) to a support-vector machine regressor (SVR). In general, this behave quite a bit better than all previous methods, as it was capable of predicting close to a full cycle with apparent correctness. 

Still, in retrospect, what this method is doing is closer to repeating the last cycle rather than predicting the next one, though this may be more than enough for various use cases, even inside FDO, as the differences between cycles is appreciable but not extremely big. Hence, for predictions in the short term, it could probably be a valid estimator, with the right hyperparameters. Still, as it can be seen on the score of the [comparison matrix](#comparisonMatrix), it can also perform pretty badly if the parameters are overfitted.

The final coded version and its results can be seen on [this notebook](/notebooks/SolarFlux_SVR_v2_month&year_features.ipynb "Fourth method notebook").

<a name="m5"></a>
### Final method: cyclical dates without outliers with SVR
Lastly, the last approach taken to predict the solar cycle was to transform the linear dates into something that could represent the cyclical nature of the problem. As read on [\(Kaleko, 2017\)](#cyclic1) and [\(London, 2017\)](#cyclic2), this meant using the sine and cosine functions to create two cyclical features to redistribute the linear data on to a circunference and to make its period the number of days of a solar cycle. The advantage of this method is that, with this data format, the SVMs can easily understand that after the 3899th day of the cycle, the next one is the 0th, and this way they can better organize its internal structure to be capable of predicting future data points.

The reason for producing two features instead of one is so that we can discriminate different dates due to the second feature breaking symmetry, that is, for example on a sine function, there are two passes over the same value on the vertical axis, so, to be able to distinguish between those points, another feature is needed, hence two features. In [this](/notebooks/Cyclical\ feature\ creation.ipynb "Cyclical feature creation") notebook it's possible to see, first, an example of this technique with hours as the only time series and how they were distributed as a clock and, later, the process and source code on how both features were created with our available data. Still, though, the basics of it can be seen in the code below.

```python
fecha_sin = [np.sin(i*(2*np.pi/3900)) for i in fechaInt]
fecha_cos = [np.cos(i*(2*np.pi/3900)) for i in fechaInt]
```

However this aproach still has a number of problems. The main one is that the period during which the solar cycle repeats is not constant and varies with time, e.i., not all cycles last the same amount of time, some solar cycles are longer than others. This poses the question of how can you make an accurate representation of it if you don't know the exact period of time. 

The approach presented above started using the mean of the solar cycle duration, which is 11 years (~4000 days), but it had the problem of offsetting itself with the available data so that, in the end, the moment of maximum activity wasn't at the start of the cycle, as it was during the first cycle, but a little less than half way through in the last one. The solution was using 3900 days as the time period instead of 4000 since this was found experimentally to not offset the data too much. Still, this would be a problem with other data sets or in large timescales, but it works pretty decently in our situation.

In conclusion, even though this final solution only uses these two features instead of all the added features from the previous methods, it achieved better predictions than all other approaches so it was the strategy later programmed into _`solarpred`_. The full notebook which served as a test run to see how it performed can be seen [here](/notebooks/SolarFlux_CycleSameAxis.ipynb "SolarFlux_CycleSameAxis notebook"), along with the obtained results.


<a name="comparisonMatrix"></a>
## Method comparison matrix

Now we will show a comparison matrix with all methods discussed in the previous section. In the table below there are two different scores from which to gather the accuracy of the prediction. 

First, there is the default scikit-learn score which is the coefficient of determination, or R^2 [\(Scikit-learn developers, R^2 score\)](#bibScores), and provides how well the samples were predicted between the output from the estimator and the historical data which was taken out of the train set. The best possible score is 1.0, and it can be negative, as the prediction can be arbitrarily bad. It should be noted that all executions were made with the same number of samples, to be able to compare between each method, even though the plots have different number of samples as they were taken before the scores.

The second score, instead, is a custom made one comparing our predictions with those given the USAF and redistributed by NOAA, speficically it is the mean squared error between the value given by our estimator and those downloaded from [this webpage](https://www.swpc.noaa.gov/products/usaf-45-day-ap-and-f107cm-flux-forecast). Unfortunately this second score was not possible to create in time, so at the moment it is to be determined, but it could be done with some fidgeting (see next chapter). It should be considered that NOAA's prediction should not be taken as the correct value but only as a reference, especially at the moment in which we are currently in the solar cycle (solar minimum), as their predictions can be extremaly faulty at times.

| Method | Historical score 						| NOAA score 	| Plot 								|
| :-:    | :-:								| :-:		| :-:								|
| m1     | -24.82713867755757						| TBD		| <img src=figures/SVRv1.png alt="plot" height="200"/> 		|
| m2  	 | -0.194096239331097						| TBD		| <img src=figures/MLPRegressor.png alt="plot" height="200"/>	|
| m3  	 | 0.04252853991520311 and 0.03941497890067924, respectively	| TBD		| <img src=figures/LinearReg.png alt="plot" height="200"/> 	|
| m4  	 | -6.716900526426215						| TBD		| <img src=figures/SVRv2.png alt="plot" height="200"/> 		|
| m5  	 | 0.46822607152875867						| TBD		| <img src=figures/SVR_cycle.png alt="plot" height="200"/> 	|


<a name="futureResearch"></a>
## Future lines of research

In this section some ideas about how the work carried out in this internship can be continued and improved upon are provided, as time forced an schedule in which not every conceived idea was followed to its fruition. As such, in no particular order, these may be some useful research lines to work on:

* Calculate the NOAA comparison score. As mentioned in the previous section, it wasn't possible to generate the score for every method tested in comparison with the NOAA predictions. This was mainly due to the data being difficult to access and process, as the predictions weren't all in a single file and the amount of data treatment which would have been needed would have been considerable. Still, once all historical predictions are obtained, calculating the score would be simple as scikit-learn provides the posibility of creating custom scores, specially as this score would only require calculation the mean squared error score between the predicted results and all NOAA predictions.

* Iterative fitting. This was first read about [here](https://www.quora.com/How-can-I-use-scikit-learn-for-data-forecasting-regression-problem), and it may be a good idea to improve the quality of the prediction on large timescales as currently _`solarpred`_ lowers the quality of its predictions every new cycle, due to they way it´s designed, as has been explained on [the final method](#m5).

* Add a feature with the sunspots number. Other solar parameter which is highly correlated with the solar flux is the number of sunspots on its surface. This information is also provided by NOAA so it could be integrated into the data to improve the prediction.

* Train with an offset of N days. This means make the algorithm predict future values of the solar flux without having the last N recent entry data points. This was considered a low priority task as the data provided by Celestrak had an offset of 1 (aka we had available all historical data from 1957 to yesterday's flux and AP index values). However it is explicitedly said on NOAA's website that recent data (<6 months old?) is provisional and could contain errors, hence why this task may still be a good idea.

* Use genetic programming (GP) to calculate the arithmetic formula of the solar cycle by means of symbolic regression instead of using numerical regression methods as it has been the case during this intership. This would provide a more transparent way of interpreting the results of the predictions because, instead of using what is mainly a black box as a support-vector machine u other methods, the GP algorithm would find the more valid coefficients for the formula using a tree representation, giving as output said formula and allowing its further study. 
For this task there have been found two python modules which could probably carry out the task: [DEAP](https://deap.readthedocs.io/en/0.7-0/examples/symbreg.html) and [gplearn](https://gplearn.readthedocs.io/en/stable/), though there may be other different frameworks which would achieve the same result.

* Use some kind of evolutionary algorithm (EA) to find the optimal time period for the creation of the date cyclical features on the final method used. As has been explained on [the final method](#m5), we create two cyclical features distributing the linear data on a circunference using the sine and cosine of the linear data and as a period the number of days of a cycle. However this number is not constant and varies with time. At the moment we use a fixed value (the mean length of a cycle of all available data) but this could be improved. One way of doing this would be calculating the optimal value for this time period using genetic algorithms u other techniques with the fitness function of the quality of the prediction.
Other way of improving this could be taking into account when each end of cycle occurs in the creation of the data and setting that as the time period for each cycle, but this would make data treatment a lot more complex.

* Apply other machine learning techniques like deep learning, specially recurrent neural networks (RNN), to create the predictor of the solar cycle.


<a name="solarpred"></a>
## _`solarpred`_ user manual

_`solarpred`_ is a python program which predicts the solar flux in the 10.7cm wavelength using a machine learning algorithm called support-vector machine regressor or SVR. It is the final implementation of the final method from the findings [section](#m5). It has been designed so that the script can take arguments in such a way that eventually it could be integrated in the workflow from FDO as an input onto the simulators of the department. The rest of this document explains how _`solarpred`_ can be installed, its functionality, the arguments it can take and how it can be improved upon in the future.

<a name="installation"></a>
### Installation

The following steps have been tested on a brand new Debian virtual machine. However, these instructions, or the equivalent, should still work on any other operative system, as they are mainly installing software dependencies, so the appropriate steps for your system should not be hard to uncover.

Firstly, we need to download the _`solarpred`_ program. This can be achieved cloning its repository on GMV's Gitlab server, [here](https://spass-git-ext.gmv.com/fdo-rd/solarpred/).

```shell
git clone https://spass-git-ext.gmv.com/fdo-rd/solarpred/
```
Once this is done, if executed as a script from the `./src/` folder, it will probably complain of some dependency not installed. Hence we download the python package manager, `pip`, to install them.

```shell
apt-get install python3-pip
```

After this has finished downloading we can install the rest of the dependencies needed by _`solarpred`_.

```shell
pip3 install sklearn numpy datetime matplotlib urllib3 joblib
apt-get install python3-tk
```

Once all of these dependencies have been downloaded and installed executing _`solarpred`_ should end succesfully, so, for example, performing a `./solarpred -D -v` should download all the data needed for the machine learning algorithms to use.

<a name="functionality"></a>
### Functionality

At the moment _`solarpred`_ can perform four main functionalities:

* First, it can download all the data needed for the machine learning algorithms to use. It also makes data treatment to it and generates a file named _data.json_ in which the treated data resides. This file consists of a JSON data structure with two keys: _'samples'_ where the proper historical data is stored and *'noaa\_predictions'* in which the USAF and NOAA predictions for the following 45 days are contained so that a score can be produced to compare our predictions to theirs.

* The second functionality is to fit a model to the data to learn how it behaves with a selected estimator. Currently, the only estimator supported is a support-vector machine regressor or SVR. This estimator has three main hyperparameters which control how it learns the data. _`solarpred`_ can also find the appropriate values for this parameters or they can be provided as arguments in the command line. Once the model has been fitted it can save the estimator to a file named _estimator.joblib_ from where it can be restored in other functionalities.

* Third, it can predict how the solar flux in the 10.7cm wavelength region will behave in the future. For this _`solarpred`_ uses the historical data downloaded and the estimator restored from the file to predict 45 days into the future. This number of days can be extended arbitrarily and the only reason it's designed like this at the moment is to be able to compare our prediction with NOAA's.

* Finally, it can perform all these three functions secuentially, downloading, executing the machine learning algorithms and predicting. This will make sure that the data and the model used for predicting are updated. Still, having the possibility to execute each task separately provides flexibility in the hypothetical integration of this tool into the simulators of FDO.

 <a name="options"></a>
### Options and execution

There are various ways to execute _`solarpred`_. If executed without arguments it will print a help message with some of the information explained in this section. Otherwise it will always have at least one argument which would be the chosen estimator which will try to fit the model to the data or one of the extra arguments below which modify the main functionality of *`solarpred`* to only download or predict. In general, the execution would follow this format:

```shell
solarpred [estimator] [estimator parameters] [extra args]
```

As stated in the previous chapter, at the moment the only estimator supported by _`solarpred`_ is the support-vector machine regressor or SVR, hence this would be the first argument, though it can probably go in other order. After the estimator has been selected, the next arguments will be its hyperparameters. In case these weren't provided _`solarpred`_ would make a extensive search to find the best possible values for each parameter, but this is not usually recommended as it takes a long time to finish. It should be noted that to mitigate this, the search space has actually been reduced and it could be much greater to find the hyperparameters with finer detail. Though in general this will not be needed, this space can be enlarged modifying the source code of the grid search.

Other extra arguments that can be provided to _`solarpred`_ are the following:

* -h, -H, --help: print a help message and exit.

* -v, -V, --verbose: set verbosity to high. Useful when debugging the application.

* -D, --download-only: only download the data to data.json and don't learn or predict.

* -L, --learn-only: only fit the model of the estimator to the data and save it to a default file. Do not download data or predict.

* -P, --predict-only: only predict using the estimator from a default file, don't fit the model to the data again or download.

<a name="futureTODO"></a>
## Future extensions to _`solarpred`_
Finally, in this section some functionality which was thought to be in _`solarpred`_ but didn't end up in the final product of the intership due to time restrictions is explained, so that it can be implemented in the future, as it will probably be of great use in the department.

* AP index prediction. The objective at the start of the internship was to be able to feed the solar flux in the 10.7 cm spectrum and the AP geomagnetic index to the models of the simulators used in FDO as both were used in the orbit decay prediction. However, to smooth the learning curve of the tools and algorightms, it was thought that it would be easier to start with only single parameter and eventually we would start working with the second one, but the intership was held before this happened. 
  Still, a small preliminary research was carried out and it was found that, first, the data was available every 3 hours, so that it would be neccesary to create other data format instead of the daily one used on F107 data, or the mean would have to be calculated. Secondly, comparing the figures from [\(Steiger, 2013\)](#apVsF107_short) and [\(Gavrilyeva and Ammosov, 2018\)](#apVsF107_long), it seemed that the flux data on 10.7cm and the AP index had a greater correlation on large timescales than in shorter ones, so the proposal would be calculating the daily mean to ease the development, but further research should probably be done. Finally, it should also be said that _`solarpred`_ already downloads both caracteristics data, but, at the moment, the AP index is not fed into the support-vector machine.

* Save estimator to a specific file. This would provide greater flexibility to _`solarpred`_ as it would be possible to tests the prediction with different hyperparameters and estimators without having to wait for the algorithms to relearn the model and without needing to fiddle with the names of different files.

* It may be a good idea to plot the same graphics used during the research phase and which can be seen on the notebooks linked above inside _`solarpred`_.

* Specific date prediction. Instead of producing always the same number of days of predicted data, it would be a good idea to be able to introduce as an input parameter the number of days, the date, or the period of time, until when we want to predict.


<a name="references"></a>
## References

<a name="svr1"></a>
Scikit-learn developers, SVR. Scikit documentation: sklearn.svm.SVR. Available in: https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html \(Reviewed April 4 2019\).

<a name="svr2"></a>
Chih-Wei, H., Chih-Chung C., Chich-Jen, L. (2016). A Practical Guide to Support Vector Classification. National Taiwan University. Available in: https://www.csie.ntu.edu.tw/~cjlin/papers/guide/guide.pdf \(Reviewed April 4 2019\).

<a name="krrsvr"></a>
Scikit-learn developers, KRR vs SVR. Scikit documentation: Comparison of kernel ridge regression and SVR. Available in: https://scikit-learn.org/stable/auto_examples/plot_kernel_ridge_regression.html \(Reviewed April 4 2019\).

<a name="kfold"></a>
Scikit-learn developers, KFold. Scikit documentation: sklearn.model_selection.KFold. Available in: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html \(Reviewed April 4 2019\).

<a name="tmsplit"></a>
Scikit-learn developers, TimeSeriesSplit. Scikit documentation: sklearn.model_selection.TimeSeriesSplit. Available in: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html \(Reviewed April 4 2019\).

<a name="mlpreg"></a> 
Scikit-learn developers, MLPRegressor. Scikit documentation: sklearn.neural_network.MLPRegressor. Available in: https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html \(Reviewed April 4 2019\).

<a name="linreg"></a>
Scikit-learn developers, Linear regression. Scikit documentation: Robust linear estimator fitting. Available in: https://scikit-learn.org/stable/modules/linear_model.html \(Reviewed April 4 2019\).

<a name="robustReg"></a>
Scikit-learn developers, Robust linear estimator fitting. Scikit documentation: Robust linear estimator fitting. Available in: https://scikit-learn.org/stable/auto_examples/linear_model/plot_robust_fit.html \(Reviewed April 4 2019\).

<a name="bibScores"></a>
Scikit-learn developers, R^2 Score. Scikit documentation: R^2 Score, the coefficient of determination. Available in: https://scikit-learn.org/stable/modules/model_evaluation.html#r2-score \(Reviewed April 30 2019\).

<a name="cyclic1"></a>
Kaleko, D. (2017). Feature Engineering - Handling Cyclical Features. Available in: http://blog.davidkaleko.com/feature-engineering-cyclical-features.html \(Reviewed April 2 2019\).

<a name="cyclic2"></a>
London, I. (2017). Encoding cyclical continuous features - 24-hour time. Available in: https://ianlondon.github.io/blog/encoding-cyclical-features-24hour-time/ \(Reviewed April 2 2019\).

<a name="apVsF107_short"></a>
Steiger, C. (2013). Low Orbit Operations of ESA's Gravity Mission GOCE. Available in: https://www.researchgate.net/figure/Average-daily-drag-compared-to-the-daily-solar-and-geomagnetic-activity-indices-F107-and_fig8_280114304 \(Reviewed April 26 2019\).

<a name="apVsF107_long"></a>
Gavrilyeva, G. and Ammosov, P. (2018). Influence of geomagnetic activity on mesopause temperature over Yakutia. Available in: https://www.researchgate.net/figure/Monthly-mean-F107-and-Ap-for-1965-2016-Both-indices-were-acquired-from-the-National_fig1_323642235 \(Reviewed April 26 2019\).


<a name="recommended"></a>
## Other recommended reading

Covas, E. et al. (2019) Neural Network Forecast of the Sunspot Butterfly Diagram. Available in: https://arxiv.org/pdf/1801.04435.pdf (Reviewed April 4 2019)

Misal, D. (2018) Using Neural Networks To Forecast Sun’s Sunspot Time Series. Available in: https://www.analyticsindiamag.com/using-neural-networks-to-forecast-suns-sunspot-time-series/ (Reviewed April 4 2019)

Roberts, S. et al. (2012) Gaussian Processes for Timeseries Modelling. Available in: http://www.robots.ox.ac.uk/~sjrob/Pubs/philTransA_2012.pdf. (Reviewed April 4 2019)
