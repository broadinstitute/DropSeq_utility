#!/usr/bin/env Rscript

library(optparse)

pArgs <- OptionParser( usage = "%prog input_reads_file input_ncells output_barcodes_file" )
#pArgs <- add_option( pArgs, type="character", action="store", dest="str_input", metavar="Input_reads", help="Input reads file." )
#pArgs <- add_option( pArgs, type="character", action="store", dest="str_input_ncells", metavar="Input_num_cells", help="Input number cells file." )
#pArgs <- add_option( pArgs, type="character", action="store", dest="str_output", metavar="Output_barcodes", help="Output barcodes." )
args <- parse_args( pArgs, positional_arguments = TRUE )

data = read.table(file=args$args[1])
Ncells = as.numeric(args$args[2])
barcodes = data$V2[1:Ncells]
write.table(as.data.frame(barcodes), file=args$args[3], col.names=FALSE, row.names=FALSE,quote=FALSE)
