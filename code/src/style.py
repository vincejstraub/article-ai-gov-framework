# Matplotlib style for Nature journal figures.
# In general, they advocate for all fonts to be panel labels to be sans serif
# and all font sizes in a figure to be 7 pt and panel labels to be 8 pt bold.

# Source: https://github.com/garrettj403/SciencePlots

# Set default figure size
figure.figsize : 3.3, 2.5 

# Font sizes
axes.labelsize: 7
xtick.labelsize: 7
ytick.labelsize: 7
legend.fontsize: 7
font.size: 7

# Font Family
font.family: sans-serif
font.sans-serif: DejaVu Sans, Arial, Helvetica, Lucida Grande, Verdana, Geneva, Lucid, Avant Garde, sans-serif
mathtext.fontset : dejavusans

# Set background color
# axes.facecolor : EFEFEF   
# figure.facecolor : EFEFEF  
# figure.edgecolor : EFEFEF   
# savefig.facecolor : EFEFEF    
# savefig.edgecolor : EFEFEF 

# Set x axis
xtick.direction : in
xtick.major.size : 3
xtick.major.width : 0.5
xtick.minor.size : 1.5
xtick.minor.width : 0.5
xtick.minor.visible : True
xtick.top : True

# Set y axis
ytick.direction : in
ytick.major.size : 3
ytick.major.width : 0.5
ytick.minor.size : 1.5
ytick.minor.width : 0.5
ytick.minor.visible : True
ytick.right : True

# Set line widths
axes.linewidth : 0.5
grid.linewidth : 0.5
lines.linewidth : 1.
lines.markersize: 3

# Remove legend frame
legend.frameon : False

# Always save as 'tight'
savefig.bbox : tight
savefig.pad_inches : 0.05