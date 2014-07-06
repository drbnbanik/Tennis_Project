###############
#This code was written to build various models with the Composite, Relational and Ecosystem attributes
##############

wd = "C:/Users/Biswanath/SkyDrive/Northwestern/Projects/Tennis/Code"
setwd(wd)
getwd()

tennis_data = read.csv("ecosystem_combined.csv", header = TRUE)
tennis_train = read.csv("ecosystem_combined_train.csv", header = TRUE)
tennis_test = read.csv("ecosystem_combined_test.csv", header = TRUE)

tennis_train_new = read.csv("def11.csv", header = TRUE)
tennis_test_new = read.csv("def21.csv", header = TRUE)

#R<-cor(tennis_train[7:34])
#R
#pairs(tennis_train[7:34])

null_model<-glm(team1_win~ 1 ,data = tennis_train, family = binomial(link = "logit"))

full_model<-glm(team1_win~ player_count_together + match_count_together + weighted_together + player_count_against + match_count_against + weighted_against + sum_height + diff_height + sum_weight + diff_weight + atleast_one_left_hand + is_same_country + past_clay_wins + past_grass_wins + past_hard_wins + recentness + last_year_clay_wins + last_year_grass_wins + last_year_hard_wins + current_year_grandslam_wins + games_played_together + games_won_together + win_rate_together + recentness_together + grass_court + hard_court ,data = tennis_train, family = binomial(link = "logit"))

stepwise_model<-step(null_model, scope=formula(full_model), direction="both", trace=0)
summary(stepwise_model)

# Stepwize model Training data misclassification rate
yhat<-predict(stepwise_model,type="response")
yhat[which(yhat>0.5)] = 1
yhat[which(yhat<0.5)] = 0
y<-tennis_train$Team1_win
sum(y != yhat)/length(y)  
# .3501984, 0.3329365
# Stepwise misclassification rate on Training data = 0.3329365, 0.3309524, 0.3501984, 0.3501984

# Stepwize model Test data misclassification rate
yhat <- predict(stepwise_model, newdata = tennis_test, type = "response")
yhat[which(yhat>0.5)] = 1
yhat[which(yhat<0.5)] = 0
y<-tennis_test$Team1_win
sum(y != yhat)/length(y) 

############################################

## Build the model with only Composite variables
full_model<-glm(team1_win~ sum_height + diff_height + sum_weight + diff_weight + atleast_one_left_hand + is_same_country + past_clay_wins + past_grass_wins + past_hard_wins + recentness + last_year_clay_wins + last_year_grass_wins + last_year_hard_wins + current_year_grandslam_wins  + grass_court + hard_court ,data = tennis_train_new, family = binomial(link = "logit"))
summary(full_model)
exp(coef(full_model)) #OR
-2*logLik(full_model)

yhat <- predict(full_model, newdata = tennis_test_new, type = "response")
yhat[which(yhat>0.5)] = 1
yhat[which(yhat<0.5)] = 0
y<-tennis_test_new$team1_win
misclassification_rate = sum(y != yhat)/length(y); misclassification_rate

tp=0;fp=0;tn=0;fn=0
for (i in 1:945){
  if (yhat[i]==0 & y[i]==1) {fn=fn+1}
  else if (yhat[i]==0 & y[i]==0) {tn = tn +1}
  else if (yhat[i]==1 & y[i] == 0) {fp = fp+1}
  else if(yhat[1]==1 & y[i]==1) {tp = tp+1}
}
tp+tn+fp+fn # check the count should come as 945
precision = tp/(tp+fp);precision
recall = tp/(tp+fn);recall
accuracy = (tp+tn)/(tp+tn+fp+fn);accuracy


## Build the model with Composite + Relational variables
full_model<-glm(team1_win~ sum_height + diff_height + sum_weight + diff_weight + atleast_one_left_hand + is_same_country + past_clay_wins + past_grass_wins + past_hard_wins + recentness + last_year_clay_wins + last_year_grass_wins + last_year_hard_wins + current_year_grandslam_wins + games_played_together + win_rate_together + recentness_together + grass_court + hard_court ,data = tennis_train_new, family = binomial(link = "logit"))
summary(full_model)

yhat <- predict(full_model, newdata = tennis_test_new, type = "response")
yhat[which(yhat>0.5)] = 1
yhat[which(yhat<0.5)] = 0
y<-tennis_test_new$team1_win
misclassification_rate = sum(y != yhat)/length(y); misclassification_rate

tp=0;fp=0;tn=0;fn=0
for (i in 1:945){
  if (yhat[i]==0 & y[i]==1) {fn=fn+1}
  else if (yhat[i]==0 & y[i]==0) {tn = tn +1}
  else if (yhat[i]==1 & y[i] == 0) {fp = fp+1}
  else if(yhat[1]==1 & y[i]==1) {tp = tp+1}
}
tp+tn+fp+fn # check the count should come as 945
precision = tp/(tp+fp);precision
recall = tp/(tp+fn);recall
accuracy = (tp+tn)/(tp+tn+fp+fn);accuracy

## Build the model with Composite+Relational+Ecosystem variables
full_model<-glm(team1_win~ player_count_together + match_count_together + weighted_together + player_count_against + match_count_against + weighted_against + sum_height + diff_height + sum_weight + diff_weight + atleast_one_left_hand + is_same_country + past_clay_wins + past_grass_wins + past_hard_wins + recentness + last_year_clay_wins + last_year_grass_wins + last_year_hard_wins + current_year_grandslam_wins + games_played_together + win_rate_together + recentness_together + grass_court + hard_court ,data = tennis_train_new, family = binomial(link = "logit"))
summary(full_model)

yhat <- predict(full_model, newdata = tennis_test_new, type = "response")
yhat[which(yhat>0.5)] = 1
yhat[which(yhat<0.5)] = 0
y<-tennis_test_new$team1_win
misclassification_rate = sum(y != yhat)/length(y); misclassification_rate

tp=0;fp=0;tn=0;fn=0
for (i in 1:945){
  if (yhat[i]==0 & y[i]==1) {fn=fn+1}
  else if (yhat[i]==0 & y[i]==0) {tn = tn +1}
  else if (yhat[i]==1 & y[i] == 0) {fp = fp+1}
  else if(yhat[1]==1 & y[i]==1) {tp = tp+1}
}
tp+tn+fp+fn # check the count should come as 945
precision = tp/(tp+fp);precision
recall = tp/(tp+fn);recall
accuracy = (tp+tn)/(tp+tn+fp+fn);accuracy

############################################################################
## Build the full model with weights or up-sampling on player_count_together
############################################################################
tennis_train_new = read.csv("def11.csv", header = TRUE)
tennis_train_new$player_count_together<-as.factor(tennis_train_new$player_count_together)
nrow(tennis_train_new)
weight<-c(rep(0,5040))

for (i in 1:5040){
  if (as.character(tennis_train_new$player_count_together[i])== as.character(0))
  {
    weight[i] = 1
  }
  else{
    weight[i] = 35 # 140:(5040-140) = 1:35
  }
}
tennis_test_new = read.csv("def21.csv", header = TRUE)
tennis_test_new$player_count_together<-as.factor(tennis_test_new$player_count_together)

#xx = glm.fit(tennis_train_new[-c(1,2,3,4,5,6,19,24,35)],tennis_train_new$team1_win,weights=weight)

full_model<-glm(team1_win~ player_count_together + match_count_together + weighted_together + player_count_against + match_count_against + weighted_against + sum_height + diff_height + sum_weight + diff_weight + atleast_one_left_hand + is_same_country + past_clay_wins + past_grass_wins + past_hard_wins + recentness + last_year_clay_wins + last_year_grass_wins + last_year_hard_wins + current_year_grandslam_wins + games_played_together + win_rate_together + recentness_together + grass_court + hard_court ,data = tennis_train_new, family = binomial(link = "logit"),weights = weight)
summary(full_model)

yhat <- predict(full_model, newdata = tennis_test_new, type = "response")
yhat[which(yhat>0.5)] = 1
yhat[which(yhat<0.5)] = 0
y<-tennis_test_new$team1_win
misclassification_rate = sum(y != yhat)/length(y); misclassification_rate

tp=0;fp=0;tn=0;fn=0
for (i in 1:nrow(tennis_test_new)){
  if (yhat[i]==0 & y[i]==1) {fn=fn+1}
  else if (yhat[i]==0 & y[i]==0) {tn = tn +1}
  else if (yhat[i]==1 & y[i] == 0) {fp = fp+1}
  else if(yhat[1]==1 & y[i]==1) {tp = tp+1}
}
tp+tn+fp+fn # check the count should be rqual to nrow(tennis_test_new)
precision = tp/(tp+fp);precision
recall = tp/(tp+fn);recall
accuracy = (tp+tn)/(tp+tn+fp+fn);accuracy


############################################################################
## Build Classification Tree on the full model
############################################################################
tennis_train_new = read.csv("def11.csv", header = TRUE)
tennis_train_new$team1_win<-as.factor(tennis_train_new$team1_win)

tennis_test_new = read.csv("def21.csv", header = TRUE)
tennis_test_new$team1_win<-as.factor(tennis_test_new$team1_win)

library(tree)
control = tree.control(nobs=nrow(tennis_train_new), mincut = 4, minsize = 8, mindev = 0.002)
#default is mindev = 0.01, which only gives a 10-node tree
tennis_train_new.tr <- tree(team1_win~ player_count_together + match_count_together + weighted_together + player_count_against + match_count_against + weighted_against + sum_height + diff_height + sum_weight + diff_weight + atleast_one_left_hand + is_same_country + past_clay_wins + past_grass_wins + past_hard_wins + recentness + last_year_clay_wins + last_year_grass_wins + last_year_hard_wins + current_year_grandslam_wins + games_played_together + win_rate_together + recentness_together + grass_court + hard_court,tennis_train_new,control=control)
tennis_train_new.tr
summary(tennis_train_new.tr)
plot(tennis_train_new.tr,type="p"); text(tennis_train_new.tr,digits=0.5, cex = 0.6)  #type="p" plots proportional branch lengths
######now prune tree and plot deviance vs. complexity parameter
tennis_train_new.tr1<-prune.tree(tennis_train_new.tr)
plot(tennis_train_new.tr1)
######now plot CV deviance vs complexity parameter
plot(cv.tree(tennis_train_new.tr, , prune.tree, K = 10))
######now find the final tree with the best value of complexity parameter
tennis_train_new.tr1<-prune.tree(tennis_train_new.tr, best = 6) #can replace replace argument "k=0.4" by "best=11" best is the best numbers of terminal nodes, k is my shrinkage parameter or lambda
tennis_train_new.tr1
summary(tennis_train_new.tr1)
plot(tennis_train_new.tr1,type="p");text(tennis_train_new.tr1,digits=1, cex = 1)

#tennis_train_new.tr2 = prune.misclass(tennis_train_new.tr, best = 6)

yhat <- predict(tennis_train_new.tr1, newdata = tennis_test_new, type = "class")
yhat<-predict(tennis_train_new.tr1, type = "class") 
yhat[which(yhat>0.5)] = 1
yhat[which(yhat<0.5)] = 0
y<-tennis_test_new$team1_win
misclassification_rate = sum(y != yhat)/length(y); misclassification_rate

tp=0;fp=0;tn=0;fn=0
for (i in 1:nrow(tennis_test_new)){
  if (yhat[i]==0 & y[i]==1) {fn=fn+1}
  else if (yhat[i]==0 & y[i]==0) {tn = tn +1}
  else if (yhat[i]==1 & y[i] == 0) {fp = fp+1}
  else if(yhat[1]==1 & y[i]==1) {tp = tp+1}
}
tp+tn+fp+fn # check the count should be rqual to nrow(tennis_test_new)
precision = tp/(tp+fp);precision
recall = tp/(tp+fn);recall
accuracy = (tp+tn)/(tp+tn+fp+fn);accuracy
