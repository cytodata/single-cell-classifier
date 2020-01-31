library(shiny)
library("RSQLite")
library(tidyverse)

ground_truth <- read_delim("ground_truth_real.csv",delim = ",")

con <- dbConnect(RSQLite::SQLite(), "scores.SQLite")

#dbRemoveTable(con, "scores")

check.model.accuracy <- function(predicted.class, actual.class){
  result.tbl <- as.data.frame(table(predicted.class,actual.class ) ) 
  
  result.tbl$Var1 <- as.character(result.tbl$predicted.class)
  result.tbl$Var2 <- as.character(result.tbl$actual.class)
  
  colnames(result.tbl)[1:2] <- c("Pred","Act")
  
  cntr <- 0  
  for (pred.class in unique(result.tbl$Pred) ){
    cntr <- cntr+ 1
    tp <- sum(result.tbl[result.tbl$Pred==pred.class & result.tbl$Act==pred.class, "Freq"])
    tp.fp <- sum(result.tbl[result.tbl$Pred == pred.class , "Freq" ])
    tp.fn <- sum(result.tbl[result.tbl$Act == pred.class , "Freq" ])
    presi <- tp/tp.fp 
    rec <- tp/tp.fn
    F.score <- if((presi+rec)==0){0}else{2*presi*rec/(presi+rec)}
    n_in_class <- tp.fn 
    if (cntr == 1 ) F.score.row <- cbind(pred.class, presi,rec,F.score,n_in_class)
    if (cntr > 1 ) F.score.row <- rbind(F.score.row,cbind(pred.class,presi,rec,F.score,n_in_class))
  }
  
  F.score.row <- as.data.frame(F.score.row) 
  return(F.score.row)
}

# Define UI for data upload app ----
ui <- fluidPage(
  
  # App title ----
  titlePanel("CytoData-2019 Scoring board"),
  
  # Sidebar layout with input and output definitions ----
  sidebarLayout(
    
    # Sidebar panel for inputs ----
    sidebarPanel(
      
      
      textInput("submissionname","Submission name [Group_ID]"),
      
      # Horizontal line ----
      tags$hr(),
      
      conditionalPanel(
        condition = 'input.submissionname != ""',
        # Input: Select a file ----
        fileInput("file1", "Choose CSV File",
                  multiple = FALSE,
                  accept = c("text/csv",
                             "text/comma-separated-values,text/plain",
                             ".csv"))
        
      ),
      
      tags$hr(),
      # Input: Checkbox if file has header ----
      checkboxInput("header", "Header", TRUE),
      
      # Input: Select separator ----
      radioButtons("sep", "Separator",
                   choices = c(Comma = ",",
                               Semicolon = ";",
                               Tab = "\t"),
                   selected = ","),
      
      # Input: Select quotes ----
      radioButtons("quote", "Quote",
                   choices = c(None = "",
                               "Double Quote" = '"',
                               "Single Quote" = "'"),
                   selected = '"'),
      
      # Horizontal line ----
      tags$hr(),
      
      # Input: Select number of rows to display ----
      radioButtons("disp", "Display",
                   choices = c(Head = "head",
                               All = "all"),
                   selected = "head"),
      
      actionButton("do", "Submit scores",icon = icon("arrow-alt-circle-right"), 
                   style="color: #fff; background-color: #337ab7; border-color: #2e6da4")
      
    ),
    
    # Main panel for displaying outputs ----
    mainPanel(
      tabsetPanel(
        tabPanel("You Uploaded", tableOutput("contents")),
        tabPanel("Summary", tableOutput("your_score"),"Table", tableOutput("error_table")),
        tabPanel("Ranking",tableOutput("all_scores"))
      )
    )
  )
)

# Define server logic to read selected file ----
server <- function(input, output) {
  output$contents <- renderTable({
    
    # input$file1 will be NULL initially. After the user selects
    # and uploads a file, head of that data file by default,
    # or all rows if selected, will be shown.
    req(input$submissionname)
    req(input$file1)
    
    # when reading semicolon separated files,
    # having a comma separator causes `read.csv` to error
    tryCatch(
      {
        df <- read.csv(input$file1$datapath,
                       header = input$header,
                       sep = input$sep,
                       quote = input$quote)
		      
        if(any(!(names(df)%in%c("cell_code","prediction")))){stop()}
        
      },
      error = function(e) {
        # return a safeError if a parsing error occurs
        stop(safeError(e))
      }
    )
    
    if(input$disp == "head") {
      return(head(df))
    }
    else {
      return(df)
    }
    
  })

    output$error_table <- renderTable({
      
      # input$file1 will be NULL initially. After the user selects
      # and uploads a file, head of that data file by default,
      # or all rows if selected, will be shown.
      req(input$submissionname)
      req(input$file1)
      # when reading semicolon separated files,
      # having a comma separator causes `read.csv` to error
      tryCatch(
        {
          df <- ground_truth %>% left_join(read.csv(input$file1$datapath,
                         header = input$header,
                         sep = input$sep,
                         quote = input$quote))


			 if(any(is.na(df$prediction))){stop()}
          error_table <- check.model.accuracy(df$prediction,df$truth) 
        },
        error = function(e) {
          # return a safeError if a parsing error occurs
          stop(safeError(e))
        }
      )
      
      if(input$disp == "head") {
        return(head(error_table))
      }
      else {
        return(error_table)
      }
      
    })
    
    output$your_score <- renderTable({
      # input$file1 will be NULL initially. After the user selects
      # and uploads a file, head of that data file by default,
      # or all rows if selected, will be shown.
      req(input$submissionname)
      req(input$file1)
          
          # when reading semicolon separated files,
          # having a comma separator causes `read.csv` to error
          tryCatch(
            {
              df <- ground_truth %>% left_join(read.csv(input$file1$datapath,
                             header = input$header,
                             sep = input$sep,
                             quote = input$quote))
			     if(any(is.na(df$prediction))){stop()}
              error_table <- check.model.accuracy(df$prediction,df$truth) 
              
                final_score <- error_table %>% tbl_df() %>% mutate_all(as.character)  %>% mutate_all(as.numeric) %>% mutate(pred.class=factor(pred.class)) %>% 
                mutate(weightedF = F.score) %>% summarise(Avg_Prec=mean(presi),Avg_Rec=mean(rec),Finalscore=sum(weightedF)/(17)) %>% mutate("Submission"=input$submissionname,"time"=Sys.time())
            },
            error = function(e) {
              # return a safeError if a parsing error occurs
              stop(safeError(e))
            }
          )
          
            return(final_score)
        })
        
      observeEvent(input$do, {
        df <- ground_truth %>% left_join(read.csv(input$file1$datapath,
                       header = input$header,
                       sep = input$sep,
                       quote = input$quote))
		       if(any(is.na(df$prediction))){stop()}
        error_table <- check.model.accuracy(df$prediction,df$truth) 
        
        final_score <- error_table %>% tbl_df() %>% mutate_all(as.character)  %>% mutate_all(as.numeric) %>% mutate(pred.class=factor(pred.class)) %>% 
          mutate(weightedF = F.score) %>% summarise(Avg_Prec=mean(presi),Avg_Rec=mean(rec),Finalscore=sum(weightedF)/(17)) %>% mutate("Submission"=input$submissionname,"time"=Sys.time())
        
        dbWriteTable(con, "scores", final_score,temporary=FALSE,append=TRUE)
        
      })
    observeEvent(input$do, {
      output$all_scores <- renderTable({
        tryCatch(
          {
        tabledf<-dbReadTable(con, "scores") %>% arrange(desc(Finalscore),desc(Avg_Prec),desc(Avg_Rec),time) %>% mutate(Rank=seq(1:n()))
        },
        error = function(e) {
          # return a safeError if a parsing error occurs
          stop(safeError(e))
        }
        )
        return(tabledf )
      })
    })
}

# Create Shiny app ----
shinyApp(ui, server)

