library(tidyverse)
library(readtext)
library(rvest)
library(tidytext)
library(quanteda)


corp_bnc<-read_html("D:\\work\\OoOM\\nlp_aspect\\bnc\\BNC2014\\spoken\\tagged\\S2A5-tgd.xml")

corp_bnc %>%
  html_nodes(xpath = "//w") %>%
  html_text %>%
  head(20)

node_u <- corp_bnc %>% html_nodes(xpath="//u")
token <- node_u %>% html_children %>% html_text
child <- node_u %>% html_children
node_u[[1]] %>% html_children %>% html_text
node_u %>% html_children %>% html_text
dim(node_u[[2]])
length(node_u)

token %>% head(10)
tags %>% head(10)

read_xml_bnc2014 <- function(xml){
  xml_file <-read_html(xml)
  node_u <- xml_file %>% html_nodes(xpath="//u")
  token_set <-c("")
  tag_set <-c("")
  for (i in 1:length(node_u)){
    token_set <- append(token_set, "</u>")
    tag_set <- append(tag_set, "PUN")
    token <- node_u[[i]] %>% html_children %>% html_text
    tags <- node_u[[i]] %>% html_children %>% html_attr("pos")
    token_set <- append(token, "</u>")
    tag_set <- append(tags, "PUN")
    token_set <- append(token_set, token)
    tag_set <- append(tag_set, tags)
  }
  return(data.frame(tag_set,token_set))
}

#corp_bnc <- read_xml_bnc2014("D:\\work\\OoOM\\nlp_aspect\\bnc\\BNC2014\\spoken\\tagged\\S2A5-tgd.xml")

bnc_flist <- dir("D:\\work\\OoOM\\nlp_aspect\\bnc\\BNC2014\\spoken\\tagged\\",full.names = T)
corp_bnc_list <- lapply(bnc_flist, read_xml_bnc2014)
corp_bnc_token_df <- corp_bnc_list %>% 
  do.call(rbind, .) %>% 
  mutate(xml_id = rep(basename(bnc_flist), sapply(corp_bnc_list,nrow)))



# save file
#write_csv(corp_bnc_token_df, path= "demo_data/data-corp-token-bnc2014.csv")
write.table(corp_bnc_token_df, "D:\\work\\OoOM\\nlp_aspect\\bnc\\BNC2014\\spoken\\BNC.spoken.csv", sep="\t", row.names=FALSE, col.names=FALSE, fileEncoding="utf-8") 