<?php

if (empty($_POST['submit'])){
    echo <<<_END
    <!DOCTYPE html>
    <html lang="en" dir="ltr">
    <head>
      <meta charset = "UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta name = "description" content = "FixTheBeats automatically arranges the notes in a MIDI file so that they fit within the range of your instrument. It then annotates the changes as lyric tags, which can be displayed in a scorewriter software.">
      <meta name = "keywords" content = "Automatic music arrangement">
      <meta name = "author" content = "Louis-Philippe Bonhomme-Beaulieu">
    <link rel="stylesheet" href="fixthebeats.css">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Special+Elite&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

        <title>Fix the Beats</title>
    </head>
      <body>

      <nav class="navbar navbar-expand-lg navbar-dark" style="background-color:#6c757d;">
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <a class="navbar-brand" href="#"></a>

        <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
          <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
            <li class="nav-item">
              <a class="nav-link" href="https://www.speakthebeats.com">Speak the Beats</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="https://www.speakthebeats.com/ReelTalk/">Reel Talk</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="https://www.speakthebeats.com/TouchdownTalk/">Touchdown Talk</a>
            </li>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="https://www.speakthebeats.com/All-TimeRhymes/">All-TimeRhymes<span class="sr-only">(current)</span></a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="https://www.speakthebeats.com/ConfidantQuotes/">Confidant Quotes</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="https://www.speakthebeats.com/SpeakTheScript/">Speak the Script<span class="sr-only">(current)</span></a>
            </li>
            <li class="nav-item active">
              <a class="nav-link" href="https://www.speakthebeats.com/FixTheBeats/">Fix the Beats<span class="sr-only">(current)</span></a>
            </li>
          </ul>
        </div>
      </nav>

    <body style="background-color:#98d3e5;">
    <div>
        <div class="container-md">
        <div class="container px-4">
        <br><br><br>
        <h1>Welcome to Fix the Beats!</h1>
        <img src="Singing cockatiel.jpg" width="650" height=auto alt="A bird singing to the beat." class="img-fluid">
        <p><b>FixTheBeats automatically arranges the notes in a MIDI file within the range of your instrument. It even annotates the MIDI file so that you can review the changes in a scorewriter software!</b></p>

        <form method = 'POST' enctype="multipart/form-data">
          <br><p>Please enter the lowest and highest notes playable on your instrument (ex: G#4 or Ab4) between A0 and G9, inclusively. Alternatively, should no notes be entered, the MIDI file will be arranged for playing on a 30 note musicbox (F scale) instead.</p>
          <div class="input-group">
            <span class="input-group-text">Lowest and Highest Notes</span>
            <input type="text" aria-label="lowest_note" class="form-control" name = "lowest_note" placeholder="Lowest">
            <input type="text" aria-label="highest_note" class="form-control" name = "highest_note" placeholder="Highest">
          </div>

          <div class="btn-group-toggle" data-toggle="buttons">
          <label class="btn btn-secondary active">
          <input type="checkbox" checked autocomplete="on" name="semitone_lock" value="semitone_lock"> Only allow octave modifications
          </label>
          </div>

          <br><p>Please specify your tempo multiplier (ex: 0.5 would increase the tempo twofold, while 2 would play at half-speed). It defaults at 1 (unchanged tempo) if no multiplier is entered.</p>
          <div class="w-50">
          <div class="input-group">
            <span class="input-group-text">Tempo multiplier</span>
            <input type="text" aria-label="tempo_multiplier" class="form-control" name = "tempo_multiplier" placeholder="must be over 0">
          </div>
          </div>


          <br><p>Please upload your MIDI (.mid) file:</p>
          <div class="input-group mb-3">
            <label class="input-group-text" for="inputGroupFile01">Upload</label>
            <input type="file" class="form-control" id="inputGroupFile01" name="MIDI_file_upload">
          </div>
        <input name = "submit" type="submit" value="Fix the Beats!" button type="button" class="btn btn-secondary btn float-right"></button>
        </form>

        <br><br>
        <div class="alert alert-secondary alert-dismissible fade show" role="alert">
             <h5>Be sure to also check out the interactive machine learning applications such as <i><b>Speak the Beats</i></b>, and related pages for movies (<i><b>Reel Talk</i></b>), Super Bowl commercials (<i><b>Touchdown Talk</i></b>), poems (<i><b>All-Time Rhymes</i></b>) and inspiring quotes (<b><i>Confidant Quotes</i></b>) and a nifty text to speech tool (<i><b>Speak the Script</i></b>) in the navbar!</h5>
             <button type="button" class="close" data-dismiss="alert" aria-label="Close">
             <span aria-hidden="true">&times;</span>
             </button>
             </div>
         </div>
        </div>
    _END;

}else{
    echo <<<_END
    <!DOCTYPE html>
    <html lang="en" dir="ltr">
    <head>
      <meta charset = "UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta name = "description" content = "FixTheBeats automatically arranges the notes in a MIDI file so that they fit within the range of your instrument. It then annotates the changes as lyric tags, which can be displayed in a scorewriter software.">
      <meta name = "keywords" content = "Automatic music arrangement">
      <meta name = "author" content = "Louis-Philippe Bonhomme-Beaulieu">
    <link rel="stylesheet" href="fixthebeats.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Special+Elite&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

    <title>Fix the Beats</title>
    </head>
    <body>

    <nav class="navbar navbar-expand-lg navbar-dark" style="background-color:#6c757d;">
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <a class="navbar-brand" href="#"></a>

      <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
        <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
          <li class="nav-item">
            <a class="nav-link" href="https://www.speakthebeats.com">Speak the Beats</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="https://www.speakthebeats.com/ReelTalk/">Reel Talk</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="https://www.speakthebeats.com/TouchdownTalk/">Touchdown Talk</a>
          </li>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="https://www.speakthebeats.com/All-TimeRhymes/">All-TimeRhymes<span class="sr-only">(current)</span></a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="https://www.speakthebeats.com/ConfidantQuotes/">Confidant Quotes</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="https://www.speakthebeats.com/SpeakTheScript/">Speak the Script<span class="sr-only">(current)</span></a>
          </li>
          <li class="nav-item active">
            <a class="nav-link" href="https://www.speakthebeats.com/FixTheBeats/">Fix the Beats<span class="sr-only">(current)</span></a>
          </li>
        </ul>
      </div>
    </nav>

    <body style="background-color:#98d3e5;">
    <div>
    <div class="container-md">
    <div class="container px-4">

    _END;
    #Extract the file extension and ensure that it is a MIDI file and that it is at most 2 MB in size.
    $file_name_and_extension = explode('.',$_FILES['MIDI_file_upload']['name']);
    $file_extension = strtolower(end($file_name_and_extension));
    if (isset($_FILES['MIDI_file_upload']) and $file_extension == "mid") {
      $file_name = substr($_FILES['MIDI_file_upload']['name'], 0, -4);
      $file_size =$_FILES['MIDI_file_upload']['size'];
      $file_tmp =$_FILES['MIDI_file_upload']['tmp_name'];

      move_uploaded_file($file_tmp,"/opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/song.mid");
      chmod ("/opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/song.mid", 0777);

    if($file_size > 2097152){
    echo <<<_END
    <br>
    <div class="card">
        <div class="card-body">
            <h2 class="card-title">File Too Large</h2>
            <hr>
            <p class="card-text"><h4>Sorry, maximal MIDI (.mid) file size is 2 MB. Please go back and try again with a smaller file.<br>
            <br>
        </div>
    </div>
    _END;
  }

    if (isset($_POST['lowest_note']) and isset($_POST['highest_note'])) {
        $lowest_note = $_POST['lowest_note'];
        $highest_note = $_POST['highest_note'];
        if (isset($_POST['tempo_multiplier'])){
            $tempo_multiplier = $_POST['tempo_multiplier'];
            if (isset($_POST['semitone_lock'])){
                $semitone_lock = $_POST['semitone_lock'];
                $command = escapeshellcmd("/home/ubuntu-server/anaconda3/bin/python3 /opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/fixthebeats.py /opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/song.mid $lowest_note $highest_note $tempo_multiplier $semitone_lock");
            }else{
                $command = escapeshellcmd("/home/ubuntu-server/anaconda3/bin/python3 /opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/fixthebeats.py /opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/song.mid $lowest_note $highest_note $tempo_multiplier");
                }
        }else{
            if (isset($_POST['semitone_lock'])){
                $semitone_lock = $_POST['semitone_lock'];
                $command = escapeshellcmd("/home/ubuntu-server/anaconda3/bin/python3 /opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/fixthebeats.py /opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/song.mid $lowest_note $highest_note $semitone_lock");
              }else{
                $command = escapeshellcmd("/home/ubuntu-server/anaconda3/bin/python3 /opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/fixthebeats.py /opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/song.mid $lowest_note $highest_note");
              }
            }
    }else{
        if (isset($_POST['tempo_multiplier'])){
            $tempo_multiplier = $_POST['tempo_multiplier'];
            if (isset($_POST['semitone_lock'])){
                $semitone_lock = $_POST['semitone_lock'];
                $command = escapeshellcmd("/home/ubuntu-server/anaconda3/bin/python3 /opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/fixthebeats.py /opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/song.mid $tempo_multiplier $semitone_lock");
            }else{
              $command = escapeshellcmd("/home/ubuntu-server/anaconda3/bin/python3 /opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/fixthebeats.py /opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/song.mid $tempo_multiplier");
            }
        }else{
            if (isset($_POST['semitone_lock'])){
                $semitone_lock = $_POST['semitone_lock'];
                $command = escapeshellcmd("/home/ubuntu-server/anaconda3/bin/python3 /opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/fixthebeats.py /opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/song.mid $semitone_lock");
            }else{
                $command = escapeshellcmd("/home/ubuntu-server/anaconda3/bin/python3 /opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/fixthebeats.py /opt/lampp/htdocs/SpeakTheBeats/FixTheBeats/song.mid");
            }
        }
        }

    $json = exec($command, $output, $return_var);
    if (strtolower($output[0][1]) == "a" or strtolower($output[0][1]) == "e") {
      $text = json_decode($json);


    echo <<<_END
      <br>
      <br>
      <h1>Fix the Beats - Here is the arranged song! </h1>

      <br>
      <div class="card">
         <div class="card-body">
             <h2 class="card-title">-Some numbers:-</h2>
             <hr>
             <p class="card-text"><h4>$text</h4></p>
         </div>
     </div>
     <br><br>
    _END;

    if (strtolower($output[0][1]) == "a"){

    echo <<<_END
     <p>Here are the two MIDI (.mid) files <b>with inferences</b>:</p>
    <a href="modified song with inferences and tags.mid" download="$file_name (modified song with inferences and tags).mid">
         <button type="button" class="btn btn-secondary btn-lg">
         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16">
     <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
     <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
     </svg> With inferences and tags</button>
     </a>
     <a href="modified song with inferences and without tags.mid" download="$file_name (modified song with inferences and without tags).mid">
         <button type="button" class="btn btn-secondary btn-lg">
         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16">
     <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
     <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
     </svg> With inferences and w/o tags</button>
     </a>

     <br><br>
     <p>Here are the two MIDI (.mid) files with <b>some of the changes converted to “O” outliers</b> if they were interspersed with unmodified notes:</p>
    <a href="modified song with outliers and tags.mid" download="$file_name (modified song with O outliers and tags).mid">
         <button type="button" class="btn btn-secondary btn-lg">
         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16">
     <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
     <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
     </svg> With “O” outliers and tags</button>
     </a>
     <a href="modified song with outliers and without tags.mid" download="$file_name (modified song with O outliers and without tags).mid">
         <button type="button" class="btn btn-secondary btn-lg">
         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16">
     <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
     <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
     </svg> With “O” outliers and w/o tags</button>
     </a>

     <br><br>
     <p>Here are the two MIDI (.mid) files <b>with changes</b>:</p>
    <a href="modified song with tags.mid" download="$file_name (modified song with tags).mid">
         <button type="button" class="btn btn-secondary btn-lg">
         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16">
     <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
     <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
     </svg> With changes and tags</button>
     </a>
     <a href="modified song without tags.mid" download="$file_name (modified song without tags).mid">
         <button type="button" class="btn btn-secondary btn-lg">
         <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16">
     <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
     <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
     </svg> With changes and w/o tags</button>
     </a>

     <br><br><br><br>
    _END;
    }
    }else{
      echo <<<_END
      <br>
      <div class="card">
          <div class="card-body">
              <h2 class="card-title">Something Went Wrong...</h2>
              <hr>
              <p class="card-text"><h4>Please go back and enter the lowest and highest notes in your instrument's range and attach a MIDI (.mid) file.<br>
              <br>
          </div>
      </div>
      _END;
     }

}else{
  echo <<<_END
  <br>
  <div class="card">
      <div class="card-body">
          <h2 class="card-title">Something Went Wrong...</h2>
          <hr>
          <p class="card-text"><h4>Please go back and enter the lowest and highest notes in your instrument's range and attach a MIDI (.mid) file.<br>
          <br>
      </div>
  </div>
  _END;
 }
 }

 ?>
