library(dplyr)
library(tidyr)
library(ggplot2)

data = read.csv("C:/Users/JackMitt/Documents/TennisBettingModel/csv_data/5.0/predictions.csv")

ah = data %>% select(Player.1.Win, Player.1.Prob) %>% drop_na() %>% arrange(Player.1.Prob)

index = seq(1, nrow(ah))

l = index[0+1:trunc(nrow(ah)/2)]
ll = l[0+1:trunc(length(l)/2)]
six = l[(trunc(length(l)/2)+1):trunc(length(l))]
lll = ll[0+1:trunc(length(ll)/2)]
five = ll[(trunc(length(ll)/2)+1):trunc(length(ll))]
llll = lll[0+1:trunc(length(lll)/2)]
four = lll[(trunc(length(lll)/2)+1):trunc(length(lll))]
lllll = llll[0+1:trunc(length(llll)/2)]
three = llll[(trunc(length(llll)/2)+1):trunc(length(llll))]
llllll = lllll[0+1:trunc(length(lllll)/2)]
two = lllll[(trunc(length(lllll)/2)+1):trunc(length(lllll))]
one = lllll[0+1:trunc(length(lllll)/2)]

r = index[(trunc(nrow(ah)/2)+1):nrow(ah)]
rr = r[(trunc(length(r)/2)+1):length(r)]
seven = r[0+1:trunc(length(r)/2)]
rrr = rr[(trunc(length(rr)/2)+1):length(rr)]
eight = rr[0+1:trunc(length(rr)/2)]
rrrr = rrr[(trunc(length(rrr)/2)+1):length(rrr)]
nine = rrr[0+1:trunc(length(rrr)/2)]
rrrrr = rrrr[(trunc(length(rrrr)/2)+1):length(rrrr)]
ten = rrrr[0+1:trunc(length(rrrr)/2)]
rrrrrr = rrrrr[(trunc(length(rrrrr)/2)+1):length(rrrrr)]
eleven = rrrrr[0+1:trunc(length(rrrrr)/2)]
twelve = rrrrr[(trunc(length(rrrrr)/2)+1):trunc(length(rrrrr))]

predictedRate = c(mean(ah$Player.1.Prob[one]),mean(ah$Player.1.Prob[two]),mean(ah$Player.1.Prob[three]),mean(ah$Player.1.Prob[four]),mean(ah$Player.1.Prob[five]),mean(ah$Player.1.Prob[six]),mean(ah$Player.1.Prob[seven]),mean(ah$Player.1.Prob[eight]),mean(ah$Player.1.Prob[nine]),mean(ah$Player.1.Prob[ten]),mean(ah$Player.1.Prob[eleven]),mean(ah$Player.1.Prob[twelve]))
actualRate = c(mean(ah$Player.1.Win[one]),mean(ah$Player.1.Win[two]),mean(ah$Player.1.Win[three]),mean(ah$Player.1.Win[four]),mean(ah$Player.1.Win[five]),mean(ah$Player.1.Win[six]),mean(ah$Player.1.Win[seven]),mean(ah$Player.1.Win[eight]),mean(ah$Player.1.Win[nine]),mean(ah$Player.1.Win[ten]),mean(ah$Player.1.Win[eleven]),mean(ah$Player.1.Win[twelve]))
n = c(length(ah$Player.1.Win[one]),length(ah$Player.1.Win[two]),length(ah$Player.1.Win[three]),length(ah$Player.1.Win[four]),length(ah$Player.1.Win[five]),length(ah$Player.1.Win[six]),length(ah$Player.1.Win[seven]),length(ah$Player.1.Win[eight]),length(ah$Player.1.Win[nine]),length(ah$Player.1.Win[ten]),length(ah$Player.1.Win[eleven]),length(ah$Player.1.Win[twelve]))
ahdf = data.frame(predictedRate,actualRate,n)

png(file="C:/Users/JackMitt/Documents/TennisBettingModel/csv_data/5.0/Calibration_Curve.png")
ggplot(ahdf, aes(y=actualRate, x=predictedRate, color = n, size = n)) + geom_point() + geom_abline(slope=1, intercept=0) + xlim(0,1) + ylim(0,1)
dev.off()





KellyDiv = 1


edge = data %>% select(Actual.Edge, My.Edge) %>% drop_na() %>% mutate(adjEdge = My.Edge/KellyDiv) %>% arrange(adjEdge)

index = seq(1, nrow(edge))

l = index[0+1:trunc(nrow(edge)/2)]
ll = l[0+1:trunc(length(l)/2)]
six = l[(trunc(length(l)/2)+1):trunc(length(l))]
lll = ll[0+1:trunc(length(ll)/2)]
five = ll[(trunc(length(ll)/2)+1):trunc(length(ll))]
llll = lll[0+1:trunc(length(lll)/2)]
four = lll[(trunc(length(lll)/2)+1):trunc(length(lll))]
lllll = llll[0+1:trunc(length(llll)/2)]
three = llll[(trunc(length(llll)/2)+1):trunc(length(llll))]
llllll = lllll[0+1:trunc(length(lllll)/2)]
two = lllll[(trunc(length(lllll)/2)+1):trunc(length(lllll))]
one = lllll[0+1:trunc(length(lllll)/2)]

r = index[(trunc(nrow(edge)/2)+1):nrow(edge)]
rr = r[(trunc(length(r)/2)+1):length(r)]
seven = r[0+1:trunc(length(r)/2)]
rrr = rr[(trunc(length(rr)/2)+1):length(rr)]
eight = rr[0+1:trunc(length(rr)/2)]
rrrr = rrr[(trunc(length(rrr)/2)+1):length(rrr)]
nine = rrr[0+1:trunc(length(rrr)/2)]
rrrrr = rrrr[(trunc(length(rrrr)/2)+1):length(rrrr)]
ten = rrrr[0+1:trunc(length(rrrr)/2)]
rrrrrr = rrrrr[(trunc(length(rrrrr)/2)+1):length(rrrrr)]
eleven = rrrrr[0+1:trunc(length(rrrrr)/2)]
twelve = rrrrr[(trunc(length(rrrrr)/2)+1):trunc(length(rrrrr))]

expectedEdge = c(mean(edge$adjEdge[one]),mean(edge$adjEdge[two]),mean(edge$adjEdge[three]),mean(edge$adjEdge[four]),mean(edge$adjEdge[five]),mean(edge$adjEdge[six]),mean(edge$adjEdge[seven]),mean(edge$adjEdge[eight]),mean(edge$adjEdge[nine]),mean(edge$adjEdge[ten]),mean(edge$adjEdge[eleven]),mean(edge$adjEdge[twelve]))
actualEdge = c(mean(edge$Actual.Edge[one]),mean(edge$Actual.Edge[two]),mean(edge$Actual.Edge[three]),mean(edge$Actual.Edge[four]),mean(edge$Actual.Edge[five]),mean(edge$Actual.Edge[six]),mean(edge$Actual.Edge[seven]),mean(edge$Actual.Edge[eight]),mean(edge$Actual.Edge[nine]),mean(edge$Actual.Edge[ten]),mean(edge$Actual.Edge[eleven]),mean(edge$Actual.Edge[twelve]))
n = c(length(edge$Actual.Edge[one]),length(edge$Actual.Edge[two]),length(edge$Actual.Edge[three]),length(edge$Actual.Edge[four]),length(edge$Actual.Edge[five]),length(edge$Actual.Edge[six]),length(edge$Actual.Edge[seven]),length(edge$Actual.Edge[eight]),length(edge$Actual.Edge[nine]),length(edge$Actual.Edge[ten]),length(edge$Actual.Edge[eleven]),length(edge$Actual.Edge[twelve]))
edgedf = data.frame(expectedEdge,actualEdge,n)

png(file="C:/Users/JackMitt/Documents/TennisBettingModel/csv_data/5.0/Edge_Graph.png")
ggplot(edgedf, aes(y=actualEdge, x=expectedEdge, color = n, size = n)) + geom_point() + geom_abline(slope=0, intercept=0, col = 'red') + geom_abline(slope=1, intercept=0) + xlim(0,0.1) + ylim(-0.2,0.2)
dev.off()