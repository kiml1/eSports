server <- function(input, output) {
  output$plot1_1 <- renderGvis({
    gvisGeoChart(plot1_1, locationvar="country", colorvar="numberPlayers",
                 options=list(width=800, height=600, colorAxis="{colors:['white', '#f73a18']}"))
  })
}

shinyApp(ui = htmlTemplate("www/index.html"), server)