#$ paths of data
datadirpythoncsv_pre = r"{./pre_tests/}"
datadirpythoncsv_post = r"{./post_tests/}"
datadirInquisitxlsx = r"{./bla/}"
datadirInquisitiqdat = r"{C:\Users\PJ\OneDrive - rwth-aachen.de\HIWI\Markus\example output\Inquisit\iqdat}"

#$ packages required
packages = c("tidyverse", "magrittr", "readxl")

for (package in packages) {
  if (!require(package, character.only = T, quietly = T)) {
    install.packages(package)
    library(package, character.only = T)
  }
}

#$ reference values for sounds
allnorms = list(
  "R_exampleI_520260520260520130130520_tapping.wav" = c(520, 260, 520, 260, 520, 130, 130, 520),
  "R_exampleII_260520650130520260260260520_tapping.wav" = c(260, 520, 650, 130, 520, 260, 260, 260, 520),
  "R_exampleIII_520650650520130390130520_tapping.wav" = c(520, 650, 650, 520, 130, 390, 130, 520),
  "R_E1_tapping.wav" = c(780, 260, 520, 260, 260, 520, 260, 260),
  "R_ES1_tapping.wav" = c(260, 260, 520, 260, 260, 520, 520),
  "R_M1_tapping.wav" = c(390, 130, 390, 130, 260, 260, 390, 130, 520),
  "R_MS2_tapping.wav" = c(260, 390, 130, 260, 260, 260, 130, 390, 260),
  "R_ES2_tapping.wav" = c(520, 260, 260, 260, 260, 520),
  "R_C2_tapping.wav" = c(130, 260, 390, 260, 130, 260, 390, 260),
  "R_MS3_tapping.wav" = c(520, 260, 130, 130, 260, 260, 260, 260, 520, 260, 130, 130),
  "R_CS1_tapping.wav" = c(260, 130, 260, 390, 260, 130, 260, 390, 260),
  "R_E2_tapping.wav" = c(520, 520, 520, 260, 260, 390, 130, 520),
  "R_ES3_tapping.wav" = c(520, 520, 520, 260, 260, 520, 520),
  "R_C1_tapping.wav" = c(260, 130, 130, 390, 130, 260, 260, 260, 130, 130),
  "R_M2_tapping.wav" = c(780, 260, 390, 390, 260, 520, 520),
  "R_MS1_tapping.wav" = c(390, 130, 260, 260, 390, 130, 260, 260, 520, 390, 130),
  "R_M3_tapping.wav" = c(520, 260, 130, 130, 260, 520, 260, 130, 390, 260, 260),
  "R_CS2_tapping.wav" = c(390, 260, 130, 260, 390, 130, 130, 260, 130, 260),
  "R_CS3_tapping.wav" = c(650, 260, 130, 390, 130, 260, 260, 650, 260, 130, 130),
  "R_E3_tapping.wav" = c(520, 260, 260, 520, 260, 260, 520, 520),
  "R_C3_tapping.wav" = c(390, 130, 260, 520, 260, 130, 390),
  "R_C_tapping.wav" = c(650,260,130,390,130,260,260,650,260,130,130),

  "TE_exampleI_129bpm_tapping.wav" = rep(465, 7),
  "TE_exampleII_116bpm_tapping.wav" = rep(517, 7),
  "TE_exampleIII_121bpm_tapping.wav" = rep(495, 7),
  "TE_MS2_tapping.wav" = rep(588, 7),
  "TE_E1_tapping.wav" = rep(545, 7),
  "TE_CS2_tapping.wav" = rep(550, 7),
  "TE_ES1_tapping.wav" = rep(461, 7),
  "TE_C1_tapping.wav" = rep(524, 7),
  "TE_ES3_tapping.wav" = rep(530, 7),
  "TE_C3_tapping.wav" = rep(512, 7),
  "TE_E2_tapping.wav" = rep(600, 7),
  "TE_MS3_tapping.wav" = rep(500, 7),
  "TE_M1_tapping.wav" = rep(480, 7),
  "TE_CS3_tapping.wav" = rep(486, 7),
  "TE_M2_tapping.wav" = rep(560, 7),
  "TE_CS1_tapping.wav" = rep(540, 7),
  "TE_ES2_tapping.wav" = rep(526, 7),
  "TE_M3_tapping.wav" = rep(533, 7),
  "TE_C2_tapping.wav" = rep(535, 7),
  "TE_MS1_tapping.wav" = rep(528, 7),
  "TE_E3_tapping.wav" = rep(520, 7)
)

analyze = function(allresults) {
  temp = allresults %>%
    group_by(sound, sbj) %>%
    slice(2:(n() - 1)) %>%
    mutate(RT = c(first(`accumulated RT`),
                  diff(`accumulated RT`)),
           ntaps = n())   %>%
    ungroup()
  
  for (sbjname in unique(temp[["sbj"]])) {
    for (soundname in unique(temp[["sound"]])) {
      nnorm = length(unlist(allnorms[soundname]))
      
      skip = unique(temp[temp$sbj == sbjname &
                           temp$sound == soundname, "ntaps"]) != nnorm
      
      temp[temp$sbj == sbjname &
             temp$sound == soundname, "skip"]  = skip
    }
  }
  
  rhythmtemp = temp[temp$block == "ritem" , ]
  tempotemp = temp[temp$block == "tempo" , ]
  
  for (soundname in unique(rhythmtemp[["sound"]])) {
    norm = allnorms[[soundname]]
    
    for (i in seq_along(norm)) {
      rhythmtemp[rhythmtemp$sound == soundname &
                   rhythmtemp$`press order` == i + 1 , "norm"] = norm [i]
    }
  }
  
  for (soundname in unique(tempotemp[["sound"]])) {
    norm = allnorms[[soundname]]
    tempotemp[tempotemp$sound == soundname, "norm"] = norm[1]
  }
  
  rhythmtemp %<>%
    group_by(sound, norm) %>%
    mutate(iqr = IQR(RT),
           q1 = quantile(RT, 1 / 4),
           q3 =  quantile(RT, 3 / 4))  %>%
    ungroup() %>%
    mutate(outlier = (RT < q1 -  3 * iqr) |
             (RT >  q3 + 3 * iqr)) %>%
    select(c("RT","skip","norm","iqr","q1","q3","outlier","sbj","sound","press order"))
  
  # identify outliers for tempo
  tempotemp %<>%
    group_by(sound) %>%
    mutate(iqr = IQR(RT),
           q1 = quantile(RT, 1 / 4),
           q3 =  quantile(RT, 3 / 4)) %>%
    ungroup() %>%
    mutate(outlier = (RT < q1 -  3 * iqr) |
             (RT >  q3 + 3 * iqr)) %>%
    select(c("RT","skip","norm","iqr","q1","q3","outlier","sbj","sound","press order"))
  
  temp = bind_rows (rhythmtemp, tempotemp)
  
  allresults %<>%
    left_join(temp, by = c("sbj", "sound", "press order")) %>%
    mutate (exclude = (outlier == TRUE))
  # lets try to ignore skip only and keep outlier only
  
  output = vector("list", length(unique(allresults[["sound"]])))
  i = 1
  
  for (sbjname in levels(allresults[["sbj"]])) {
    for (blockname in levels(allresults[["block"]])) {
      for (phasename in levels(allresults[["phase"]])) {
        selectedresults = allresults[(allresults$sbj == sbjname) &
                                       (allresults$block == blockname) &
                                       (allresults$phase == phasename), ]
        
        for (soundname in unique(selectedresults[["sound"]])) {
          onetrial =  selectedresults[selectedresults$sound == soundname,] # data for current sound
          exclude = onetrial[["exclude"]]  %>% .[2:(length(.) - 1)] %>%  any()
          # exclude = FALSE
          
          onetrialnorm = allnorms[[soundname]] # reference values for current sound
          
          RTveccumulative = onetrial[["accumulated RT"]]  %>%
            .[2:(length(.) - 1)] # drop the first and the last RT for current sound
          
          if (blockname == "ritem") {
            ##| analyze rhythm
            
            if (exclude) {
              # analysis skipped because of wrong tapping number or outliers
              
              AbsoluteAsynchrony = NA
              RelativeAsynchrony = NA
              AbsoluteCorrectness = NA
              RelativeCorrectness = NA
            } else {
              # analysis not skipped because of correct tapping number
              
              RTvec = c(RTveccumulative[1], diff(RTveccumulative)) # vector of RT intervals
              
              Absolutediffthreshold = onetrialnorm %>%
                sort() %>%
                diff() %>%
                abs() %>%
                .[. != 0] %>%
                min() / 2 + 1
              
              AbsoluteCorrectness = all(abs(RTvec - onetrialnorm) < Absolutediffthreshold)
              
              RTveccumulativerelative = RTveccumulative / tail(RTveccumulative, n =
                                                                 1)
              
              onetrialnormcumulative = cumsum(onetrialnorm)
              
              onetrialnormrelative = onetrialnorm /  sum(onetrialnorm)
              
              onetrialnormcumulativerelative = cumsum (onetrialnormrelative)
              
              Relativediffthreshold = onetrialnormrelative %>%
                sort() %>%
                diff() %>%
                abs() %>%
                .[. != 0] %>%
                min() / 2
              
              RelativeCorrectness = all(
                abs(
                  onetrialnormcumulativerelative -  RTveccumulativerelative
                ) < Relativediffthreshold
              )
              
              AbsoluteAsynchrony = mean(abs(RTveccumulative - onetrialnormcumulative) /
                                          onetrialnorm)
              
              RelativeAsynchrony =  (
                abs(
                  RTveccumulativerelative - onetrialnormcumulativerelative
                ) / onetrialnormrelative
              ) %>%
                .[-length(.)] %>%
                mean()
            }
            
            ##| save analysis results
            output[[i]] = c(
              onetrial[1, ][c("sbj" ,
                              "age" ,
                              "sex" ,
                              "block" ,
                              "phase" ,
                              "trialnr" ,
                              "sound")] ,
              c(
                "exclude" = exclude,
                "AbsoluteAsynchrony" = AbsoluteAsynchrony,
                "RelativeAsynchrony" = RelativeAsynchrony,
                "AbsoluteCorrectness" = AbsoluteCorrectness,
                "RelativeCorrectness" = RelativeCorrectness
              )
            )
            i = i + 1
          } else if (blockname == "tempo") {
            ##| analyze tempo
            
            if (exclude) {
              # analysis skipped because of wrong tapping number or outliers
              
              Asynchrony = NA
            } else {
              # analysis not skipped because of correct tapping number
              
              RTvec = c(RTveccumulative[1], diff(RTveccumulative)) # vector of RT intervals
              
              Asynchrony = mean(abs(onetrialnorm - RTvec) / onetrialnorm)
            }
            
            ##| save analysis results
            output[[i]] = c(onetrial[1, ][c("sbj" ,
                                            "age" ,
                                            "sex" ,
                                            "block" ,
                                            "phase" ,
                                            "trialnr" ,
                                            "sound")] ,
                            c("exclude" = exclude,
                              "Asynchrony" = Asynchrony))
            i = i + 1
          }
        }
      }
    }
  }
  
  output = bind_rows(output)
  
  return(output)
  
}

##| analyze python csv
if (dir.exists(datadirpythoncsv_pre)) {
  ###| read python csv
  files = list.files(
    path = datadirpythoncsv_pre,
    pattern = "*.csv",
    full.names = TRUE,
    recursive = FALSE
  )
  
  if (length(files) > 0) {
    allresultspythoncsv = vector("list", length(files))
    
    for (i in seq_along(files)) {
      one = read_delim(
        files[i],
        delim = "; ",
        col_names = TRUE,
        trim_ws = TRUE,
        col_types = cols(.default = col_character())
      )
      
      allresultspythoncsv[[i]] = one
    }
    allresultspythoncsv = bind_rows(allresultspythoncsv)
  }
  ####| specify column name & data type
  vartypes = cols(
    sbj = col_factor(levels = NULL, ordered = FALSE),
    age = col_integer(),
    sex = col_factor(levels = NULL, ordered = FALSE),
    block = col_factor(levels = NULL, ordered = FALSE),
    phase = col_factor(levels = NULL, ordered = FALSE),
    trialnr = col_integer(),
    sound = col_factor(levels = NULL, ordered = FALSE),
    'press order' = col_integer(),
    'accumulated RT' = col_integer(),
    'press duration' =  col_integer(),
    'key name' = col_factor(levels = NULL, ordered = FALSE)
  )
  
  allresultspythoncsv = type_convert(allresultspythoncsv,
                                     col_types = vartypes)
  
  outputpythoncsv_pre = analyze(allresultspythoncsv)
  View(outputpythoncsv_pre)
}

##| analyze python csv
if (dir.exists(datadirpythoncsv_post)) {
  ###| read python csv
  files = list.files(
    path = datadirpythoncsv_post,
    pattern = "*.csv",
    full.names = TRUE,
    recursive = FALSE
  )
  
  if (length(files) > 0) {
    allresultspythoncsv = vector("list", length(files))
    
    for (i in seq_along(files)) {
      one = read_delim(
        files[i],
        delim = "; ",
        col_names = TRUE,
        trim_ws = TRUE,
        col_types = cols(.default = col_character())
      )
      
      allresultspythoncsv[[i]] = one
    }
    allresultspythoncsv = bind_rows(allresultspythoncsv)
  }
  ####| specify column name & data type
  vartypes = cols(
    sbj = col_factor(levels = NULL, ordered = FALSE),
    age = col_integer(),
    sex = col_factor(levels = NULL, ordered = FALSE),
    block = col_factor(levels = NULL, ordered = FALSE),
    phase = col_factor(levels = NULL, ordered = FALSE),
    trialnr = col_integer(),
    sound = col_factor(levels = NULL, ordered = FALSE),
    'press order' = col_integer(),
    'accumulated RT' = col_integer(),
    'press duration' =  col_integer(),
    'key name' = col_factor(levels = NULL, ordered = FALSE)
  )
  
  allresultspythoncsv = type_convert(allresultspythoncsv,
                                     col_types = vartypes)
  
  outputpythoncsv_post = analyze(allresultspythoncsv)
  View(outputpythoncsv_post)
}


#$ reformat Inquisit data as python csv
reformatInquisit =  function(allresults) {
  allresults  %<>%
    mutate(sound = case_when(.$trialcode %in% c("listen") ~  stimulusitem1)) %>%
    fill(sound) %>%
    .[.$trialcode %in% c("tap"), ] %>%
    mutate(
      age = NA,
      sex = NA,
      trialnr = NA,
      'press duration' = NA,
      'key name' = NA
    ) %>%
    rename(sbj = subject, RT = latency) %>%
    group_by(sbj, sound) %>%
    mutate(
      tempstring = substr(stimulusitem1, 1, 20) ,
      # stimulusitem1 contains instructions indicating phase and block
      phase = if_else(
        grepl("Practice", tempstring, ignore.case = T) ,
        "practice",
        "testing"
      ),
      block = case_when(
        grepl("Rhythm", tempstring, ignore.case = T) ~ "ritem",
        grepl("Tempo", tempstring, ignore.case = T) ~ "tempo"
      ) ,
      'press order' = row_number()
    ) %>%
    dplyr::mutate('accumulated RT' = cumsum(RT) - first(RT))
  
  # specify column name & data type
  vartypes = cols(
    sbj = col_factor(levels = NULL, ordered = FALSE),
    #todo sbj to factor not working!
    age = col_integer(),
    sex = col_factor(levels = NULL, ordered = FALSE),
    block = col_factor(levels = NULL, ordered = FALSE),
    phase = col_factor(levels = NULL, ordered = FALSE),
    trialnr = col_integer(),
    sound = col_factor(levels = NULL, ordered = FALSE),
    'press order' = col_integer(),
    'accumulated RT' = col_integer(),
    'press duration' =  col_integer(),
    'key name' = col_factor(levels = NULL, ordered = FALSE)
  )
  
  allresults = type_convert(allresults,
                            col_types = vartypes)
  
  allresults$sbj %<>% as_factor()
  return(allresults)
}

##| analyze Inquisit xlsx

if (dir.exists(datadirInquisitxlsx)) {
  ###| read Inquisit xlsx
  files = list.files(
    path = datadirInquisitxlsx,
    pattern = "*.xlsx",
    full.names = TRUE,
    recursive = FALSE
  )
  
  if (length(files) > 0) {
    allresultsInquisitxlsx = vector("list", length(files))
    
    
    for (i in seq_along(files)) {
      one = read_excel(
        files[i],
        col_names = TRUE,
        trim_ws = TRUE,
        col_types = "guess"
      )
      
      allresultsInquisitxlsx[[i]] = one
    }
    
    allresultsInquisitxlsx = bind_rows(allresultsInquisitxlsx)
    
  }
  
  allresultsInquisitxlsx %<>% reformatInquisit ()
  
  outputInquisitxlsx = analyze(allresultsInquisitxlsx)
  View(outputInquisitxlsx)
}

##| analyze Inquisit iqdat

if (dir.exists(datadirInquisitiqdat)) {
  ###| read Inquisit iqdat
  files = list.files(
    path = datadirInquisitiqdat,
    pattern = "*.iqdat",
    full.names = TRUE,
    recursive = FALSE
  )
  
  if (length(files) > 0) {
    allresultsInquisitiqdat = vector("list", length(files))
    
    for (i in seq_along(files)) {
      one = read_delim(
        files[i],
        delim = "\t",
        col_names = TRUE,
        trim_ws = TRUE,
        col_types = NULL,
        show_col_types = FALSE
      )
      
      allresultsInquisitiqdat[[i]] = one
    }
    allresultsInquisitiqdat = bind_rows(allresultsInquisitiqdat)
  }
  
  allresultsInquisitiqdat %<>% reformatInquisit ()
  
  outputInquisitiqdat = analyze(allresultsInquisitiqdat)
  View(outputInquisitiqdat)
}
