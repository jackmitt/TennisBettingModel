library(dplyr)
library(tidyr)
library(ggplot2)
library(GGally)
library(useful)
library(cluster)
library(factoextra)

dataAll = read.csv("C:/Users/JackMitt/Documents/TennisBettingModel/playersForKNN.csv")
data = scale(read.csv("C:/Users/JackMitt/Documents/TennisBettingModel/playersForKNN.csv")[-c(1)])
rownames(data) = dataAll$Player

#elbow method for determining num clusters
totwss = c()
for (k in 1:10){
  data.km = kmeans(data, centers=k, nstart=25)
  totwss=c(totwss, data.km$tot.withinss)
}
dat = data.frame(NumCluster=1:10, totwss=totwss)
ggplot(dat, aes(x=NumCluster, y=totwss)) + geom_point() + geom_line() + scale_x_continuous(breaks=seq(0,10,1)) + xlab("Number of clusters") + ylab("Total within-cluster sum of squares") + theme_bw()

#kmeans
set.seed(1234)
datak4 = kmeans(data, centers=4, nstart=25)
datak4$cluster = as.factor(datak4$cluster)
datak4centers = data.frame(1:4, datak4$centers)
colnames(datak4centers)[1] = "cluster"
datak4centers$cluster = as.factor(datak4centers$cluster)
ggparcoord(datak4centers, columns=2:20, groupColumn = 1) + theme_bw()

plot(datak4, data=data)



#Principal Component Analysis
dat.pca = prcomp(data)
fviz_pca_biplot(dat.pca, col.ind=datak4$cluster, col.var="black", legend.title="Cluster", repel=TRUE)
