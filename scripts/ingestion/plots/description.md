**evolve\_in**

The graph shows the temporally increasing number of dependencies based on in-degree of the top 10 packages for the "amd64" architecture. It shows how many other packages are depended on this package to run. Any vulnerability in this package could lead to significant loss in many other dependent packages. 

- X axis denotes the months
- Y axis denotes the In-degree (Number of dependencies of a module)


**On in-degree graphs:**

Package behavior is unpredictable; many of the popular packages from 2017—such as "mawk 1.3.3-17+b3," "libsigsegv2 2.12-2," "dh-autoreconf 19," and "autotools-dev 20180224.1"—aren’t so popular in 2020. They are not even listed among the top ten packages for 2020–2022. We can also remark that the usage of "libsub-override-perl 0.09-2" and "intltool-debian 0.35.0+20060710.5," packages is also decreased. 

We can say that the usage of packages or building the new packages varied a lot from 2020, because of which we can find many new packages like ‘zliblg\_1:1.2.11.dfsg-2’,’ libnsl2\_1.3.0-2’, ‘libnsl-dev\_1.3.0-2’ and ‘libmpfr6\_4.1.0-3’ in the top list. There is huge increase in the usage of ‘hostname\_3.23’ and ‘lsb-base\_11.1.0’ packages.

**evolve\_out.png**

The graph shows the temporally increasing number of dependencies based on out-degree of the top 10 packages for the "amd64" architecture. It shows how many dependent packages are needed to run the primary package. These packages come with a high risk because even a minor vulnerability in any of the dependent package could lead to a significant loss.

- X axis denotes the months
- Y axis denotes the Out-degree (Number of dependencies of a module)


**On out-degree graphs:**

From 2017 to 2022, the "evolution," "plasma-desktop," and "libreoffice" packages had the same usage. This is conceivable since they appear in both graphs at the same ranking position.

Between 2017 and 2020, usage of "gnome-shell," "virtualbox," "gnome-control-center," "plasma-workspace," and "binutils" has been noticeably increased. The use of a few other new packages, such as "calamares," "thunderbird," and "kdenlive," has increased notably.

From 2017 to 2022, "kdeplasma-addons" usage decreased significantly. Due to this, it suddenly rose from fifth to tenth place in 2020. This indicates that it is widely used between 2017 and 2019 because of which it has the highest out-degree. Or we could remark that more people are using other packages besides this one. For them to arrive in advance of these packages. 

Although "webkit2gtk" is one of the most connected package from 2017 to 2022, this package is not included in the 2020 to 2022 graph, indicating that it was not utilized much after 2020.









**Statistical Measures**

The graph demonstrates a descriptive analysis of the packages using logarithms to depict the statistical data for each quarter.

- X axis denotes the quarter.
- Y axis denotes the descriptive values

In all the cases with respective to quarterly analysis the **minimum degree** of the package and the **logarithm of 25th percentile** of the packages are having their value as ‘0’ and remained same throughout the analysis which means many packages have their degree <10 (i.e. they are connected to less than 10 packages which also indicate there are many independent packages or many packages which has less risk). Speaking of **logarithm of** **median** in some cases we can find a small shift (0-1) initially or it remained constant (either 0 or 1) throughout the analysis which again indicates that many (50% or more) packages have 0-99 dependency packages connected to them. Coming to **logarithm of 75th percentile** of the packages are having their values around 0 or 2 which still indicates that (nearly 1779033 packages) have 0-999 dependency packages connected to them.

The **logarithm of mean** either remained fairly constant across the plots or varied slightly in the middle. Comparing the logarithm of 75th percentile (which is around 2) and the mean values, which in most cases ranged about "4", indicate that there are primary packages with very high dependent packages connected to it. This increased the mean value to "4". When it comes to the **logarithm of the maximum degree** of packages, there was little variation in the middle, but the value was consistently higher than "8." However, if we look at the maximum degree's normal values, we see that its value gradually increased throughout the period. 

**In-degree Graphs**

For in-degree plots, the **logarithm of standard deviation** showed numerous fluctuations. The midst of them had sharp drops. The **maximum in-degree** of the packages also exhibited similar behavior, which reminds us that developers tried or started to develop independent packages to reduce risk at various phases (quarters). But as time went on, they once more relied on other packages to integrate new features.

**Out-degree Graphs**

The **logarithm of standard deviation** and **maximum out-degree** showed gradual increase in their values.
