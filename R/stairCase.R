
getColors <- function() {
  
  cols.op <- c(rgb(255, 147, 41,  255, max = 255), # orange:  21, 255, 148
               rgb(229, 22,  54,  255, max = 255), # red:    248, 210, 126
               rgb(207, 0,   216, 255, max = 255), # pink:   211, 255, 108
               rgb(127, 0,   216, 255, max = 255), # violet: 195, 255, 108
               rgb(0,   19,  136, 255, max = 255)) # blue:   164, 255, 68
  
  cols.tr <- c(rgb(255, 147, 41,  32,  max = 255), # orange:  21, 255, 148
               rgb(229, 22,  54,  32,  max = 255), # red:    248, 210, 126
               rgb(207, 0,   216, 32,  max = 255), # pink:   211, 255, 108
               rgb(127, 0,   216, 32,  max = 255), # violet: 195, 255, 108
               rgb(0,   19,  136, 32,  max = 255)) # blue:   164, 255, 68
  
  cols <- list()
  cols$op <- cols.op
  cols$tr <- cols.tr
  
  return(cols)
  
}


plotFile <- function(filename, independent='duration') {
  
  
  # there are two variables we can play with:
  # - duration
  # - strength (amplitude?)
  # but not frequency!
  
  # read the data
  df <- read.csv(filename, header=TRUE, stringsAsFactors=FALSE)
  
  if (independent == 'duration') {
    groupby='strength'
  }
  if (independent == 'strength') {
    groupby='duration'
  }
  
  # create plot
  xrange <- range(df[[independent]])
  plot(NULL,NULL,
       main='',xlab=independent,ylab='proportion yes responses',
       xlim=xrange, ylim=c(0,1),
       ax=F,bty='n')
  
  
  colors <- getColors()
  
  groupbyvals <- sort(unique(df[[groupby]]))
  
  for (sub_no in c(1:length(groupbyvals))) {
    sub = groupbyvals[sub_no]
    subdf <- df[df[[groupby]] == sub,]
    
    agg_resp <- aggregate(response ~ subdf[[independent]], data=subdf, FUN=mean)
    # plot the data
    # lines(agg_resp[[1]], agg_resp$response, type='b', pch=19, lwd=1, col=colors$op[sub_no])
    lines(agg_resp[[1]], agg_resp$response, lwd=1, col=colors$op[sub_no])
  }
  
  legend(6,1,legend=groupbyvals, col=colors$op, lwd=1, bty='n', cex=0.8, title=groupby)
  
  axis(side=1, at=seq(xrange[1], xrange[2], length.out=5), cex.axis=0.8)
  axis(side=2, at=c(0,0.5,1), cex.axis=0.8)
  
}