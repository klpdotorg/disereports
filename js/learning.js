var info;
var translations;

// Load the Visualization API and the piechart package.
google.load('visualization', '1', {'packages':['corechart','table','imagechart']});
var table1;
var grades = ['Z','L','W','S','P'];
var grade_labels = {'Z':'Zero','L':'Letter','W':'Word','S':'Sentence','P':'Paragraph'};

String.prototype.toTitleCase = function () {
    return this.replace(/\w\S*/g, function(txt){
      if(txt.indexOf('/')>0)
        return txt;
      else
	return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
};

function logslider(position) {
  // position will be between 0 and 100
  var minp = 0;
  var maxp = 100;

  // The result should be between 1 an 200
  var minv = Math.log(3);
  var maxv = Math.log(300);

  // calculate adjustment factor
  var scale = (maxv-minv) / (maxp-minp);

  return Math.exp(minv + scale*(position-minp));
}

    
function initialise(data)
{
  info = data;
  translations = info['transdict'];
  now = new Date()
  document.getElementById("reportdate").innerHTML = now.toDateString();
  document.getElementById("rephead").innerHTML = "<img src=\'/images/KLP_logo2.png\' width='130px' vertical-align='top' border=0 />" + '<br/>' + translations['H56'];

  document.getElementById("constname").innerHTML = translations[info["const_type"]] + " <img src=\'/images/arrow.gif\' width='8px' vertical-align='center' border='0'/>" + "<br/><h1>"  
                                               + info['const_name'] + "</h1>";
  document.getElementById("constinfo").innerHTML =  "<dl class='header-def'><dt>" + translations['H8'] + "</dt><dd>"
                           + info["const_code"] + "</dd>"
                           + "<dt>" + translations['H9'] + "</dt><dd>" + info["const_rep"] + "</dd>"
                           + "<dt>" + translations['H10'] + "</dt><dd>" + info["const_party"] + "</dd>" 
			   + "</dl>";
  document.getElementById("hiddenip").innerHTML = '<input type="hidden" name="const_type" value="'+ info["constype"] + '" />' +
  '<input type="hidden" name="const_id" value="'+ info["const_id"] + '" />' +
  '<input type="hidden" name="forreport" value="'+ info["forreport"] + '" />' +
  '<input type="hidden" name="rep_lang" value="'+ info["rep_lang"] + '" />' ;
  document.getElementById('instcounts').innerHTML = '<dl class=\'header-def\'>' 
			   + '<dt style="font-size:9pt">' + translations['H11'] + '</dt>'
                           + '<dd>' + info["inst_counts"]["abs_schcount"] + '</dd>'
			   + '<dt style="font-size:9pt">' + translations['H12'] + '</dt>'
                           + '<dd>' + info["inst_counts"]["abs_preschcount"] + '</dd>'
                           + '</dl>'
  if(parseInt(info["lib_count"]) != 0){
  
    document.getElementById("learninghead").innerHTML = translations['H113'];
    document.getElementById('learningintro_txt').innerHTML = (info['learningintro_txt'] == 'undefined') ? translations['H60'] : info['learningintro_txt'];

    document.getElementById('schassess_txt').innerHTML = (info['schassess_txt'] == 'undefined') ? translations['H60'] : info['schassess_txt'];
    document.getElementById('schgph_txt').innerHTML = (info['schgph_txt'] == 'undefined') ? translations['H60'] : info['schgph_txt'];
    if(Object.keys(info["sch_assess_class"]).length > 0)
    {
      sch_assess_chart();
    } else {
      document.getElementById('schassessclass_gph').innerHTML = '<br/><br/><b>' + translations['H119'] + '</b><br/>' ;
      sch_blore_chart();
    }

    document.getElementById("angassesshead").innerHTML = translations['H114'];
    document.getElementById('angassess_txt').innerHTML = (info['angassess_txt'] == 'undefined') ? translations['H60'] : info['angassess_txt'];
    document.getElementById('angexpln_txt').innerHTML = (info['angexpln_txt'] == 'undefined') ? translations['H60'] : info['angexpln_txt'];
    if(info["ang_assess_score"] !=undefined )
    {
      document.getElementById('angassessmore_txt').innerHTML = (info['angassessmore_txt'] == 'undefined') ? translations['H60'] : info['angassessmore_txt'];
      ang_assess_chart();
    } else {
      document.getElementById('angassessmore_txt').innerHTML = (info['angassessmore_txt'] == 'undefined') ? translations['H60'] : info['angassessmore_txt'] + '<br/><br/><b>' + translations['H120'] + '</b><br/>';
      ang_blore_only();
    }

    document.getElementById('source_txt').innerHTML = (info['source_txt'] == 'undefined') ? translations['H60'] : info['source_txt'];
  }
}

function sch_assess_chart()
{
      var data = new google.visualization.DataTable();
      data.addColumn('string' , 'Class');
      for (var i in grades) {
          data.addColumn('number', grade_labels[grades[i]]);
      }
      for (var key in info["sch_assess_class"]){
        row = ['Class ' + key]
        values = []
        for (var i in grades) {
            score = info["sch_assess_class"][key][grades[i]] == undefined ? 0 : info["sch_assess_class"][key][grades[i]];
            score = score / info["sch_assess_class"][key]["total"] * 100;
            values.push(score);
        }
        //alert(values);
        //alert(roundPerc(values,100));
        data.addRow(row.concat(roundPerc(values,100)));
      }
      data.sort([{column:0,desc:false}]);
      var chart1 = new google.visualization.BarChart(document.getElementById('schassessclass_gph'));
      chart1.draw(data, {width: 750, height: 250, chartArea:{width:'70%'},  title: translations['H115'],colors:['E6550D','FDAE6B','FFEDA0','ADDD8E','31A354'], isStacked:true});

      data = new google.visualization.DataTable();
      data.addColumn('string' , 'Gender');
      for (var i in grades) {
          data.addColumn('number', grade_labels[grades[i]]);
      }
      for (var key in info["sch_assess_gender"]){
        row = [key.toUpperCase()+'S']
        values = []
        for (var i in grades) {
            score = info["sch_assess_gender"][key][grades[i]] == undefined ? 0 : info["sch_assess_gender"][key][grades[i]];
            score = score / info["sch_assess_gender"][key]["total"] * 100;
            values.push(score);
        }
        data.addRow(row.concat(roundPerc(values,100)));
      }
      data.sort([{column:0,desc:false}]);
      var chart1 = new google.visualization.BarChart(document.getElementById('schassessgend_gph'));
      chart1.draw(data, {width: 750, height: 150, bar:{groupWidth:'35%'},chartArea:{width:'70%'},  title: translations['H116'],colors:['E6550D','FDAE6B','FFEDA0','ADDD8E','31A354'], isStacked:true});

      data = new google.visualization.DataTable();
      data.addColumn('string' , 'Constituency');
      for (var i in grades) {
          data.addColumn('number', grade_labels[grades[i]]);
      }
      row = [info['const_name'].toTitleCase()]
      values = []
      for (var i in grades) {
          score = info["sch_assess_const"][grades[i]] == undefined ? 0 : info["sch_assess_const"][grades[i]];
          score = score * 100/ info["sch_assess_const"]["total"];
          values.push(score);
      }
      data.addRow(row.concat(roundPerc(values,100)));
      row = ['Bangalore']
      values = []
      for (var i in grades) {
          score = info["sch_assess_bang"][grades[i]] == undefined ? 0 : info["sch_assess_bang"][grades[i]];
          score = score * 100/ info["sch_assess_bang"]["total"];
          values.push(score);
      }
      data.addRow(row.concat(roundPerc(values,100)));
      row = ['Karnataka Rural']
      data.addRow(row.concat(roundPerc([5.26,15.16,16.68,19.11,43.79],100)));

      //data.sort([{column:0,desc:false}]);
      var chart1 = new google.visualization.BarChart(document.getElementById('schassesscomp_gph'));
      chart1.draw(data, {width: 750, height: 180, bar:{groupWidth:'45%'},chartArea:{width:'70%'},  title: translations['H118'],colors:['E6550D','FDAE6B','FFEDA0','ADDD8E','31A354'],isStacked:true});
}

function sch_blore_chart()
{
      var data = new google.visualization.DataTable();
      data.addColumn('string' , 'Constituency');
      for (var i in grades) {
          data.addColumn('number', grade_labels[grades[i]]);
      }
      row = ['Bangalore']
      values = []
      for (var i in grades) {
          score = info["sch_assess_bang"][grades[i]] == undefined ? 0 : info["sch_assess_bang"][grades[i]];
          score = score * 100/ info["sch_assess_bang"]["total"];
          values.push(score);
      }
      data.addRow(row.concat(roundPerc(values,100)));
      row = ['Karnataka Rural']
      data.addRow(row.concat(roundPerc([5.26,15.16,16.68,19.11,43.79],100)));

      var chart1 = new google.visualization.BarChart(document.getElementById('schassesscomp_gph'));
      chart1.draw(data, {width: 750, height: 150, bar:{groupWidth:'35%'},chartArea:{width:'70%'},  title: translations['H121'],colors:['E6550D','FDAE6B','FFEDA0','ADDD8E','31A354'],isStacked:true});
}

function ang_assess_chart()
{
     var svghtml= '<svg width="100%" height="210px" width="400px" version="1.0" xmlns="http://www.w3.org/2000/svg">'
     var _cx = 180;
     var _cy = 100;
     var bang_r = info["ang_assess_bang"]
     svghtml = svghtml + drawCircle(_cx,_cy,bang_r,'Bangalore','#CCC');
     svghtml = svghtml + '</svg>';
     document.getElementById('angassessbang_gph').innerHTML = svghtml

     svghtml= '<svg width="100%" height="210px" width="400px" version="1.0" xmlns="http://www.w3.org/2000/svg">'
     _cx = 180;
     _cy = 100;
     var const_r = info["ang_assess_score"];
     if (const_r > bang_r) {
       svghtml = svghtml + drawCircle(_cx,_cy,const_r,info["const_name"].toTitleCase(),'#31A354');
     } else {
       svghtml = svghtml + drawCircle(_cx,_cy,const_r,info["const_name"].toTitleCase(),'#E6550D');
     }
     svghtml = svghtml + '</svg>';
     document.getElementById('angassess_gph').innerHTML = svghtml

     var br = info["ang_assess_gender"]["male"];
     var gr = info["ang_assess_gender"]["female"];
     var bbr = info["ang_assess_bang_gender"]["male"];
     var bgr = info["ang_assess_bang_gender"]["female"];
     document.getElementById('angassess_boy').innerHTML = drawIcons(br,gr,bbr,bgr,1,'B');
     document.getElementById('angassess_girl').innerHTML = drawIcons(br,gr,bbr,bgr,1,'G');
     document.getElementById('angassess_bang_boy').innerHTML = drawIcons(br,gr,bbr,bgr,2,'B');
     document.getElementById('angassess_bang_girl').innerHTML = drawIcons(br,gr,bbr,bgr,2,'G');
}

function ang_blore_only()
{
     var svghtml= '<svg width="100%" height="210px" width="400px" version="1.0" xmlns="http://www.w3.org/2000/svg">'
     var _cx = 180;
     var _cy = 100;
     var bang_r = info["ang_assess_bang"]
     svghtml = svghtml + drawCircle(_cx,_cy,bang_r,'Bangalore','#CCC');
     svghtml = svghtml + '</svg>';
     document.getElementById('angassessbang_gph').innerHTML = svghtml
     var bbr = info["ang_assess_bang_gender"]["male"];
     var bgr = info["ang_assess_bang_gender"]["female"];
     var br = 0;
     var gr = 0; 
     var bbr = info["ang_assess_bang_gender"]["male"];
     var bgr = info["ang_assess_bang_gender"]["female"];
     document.getElementById('angassess_bang_boy').innerHTML = drawIcons(br,gr,bbr,bgr,2,'B');
     document.getElementById('angassess_bang_girl').innerHTML = drawIcons(br,gr,bbr,bgr,2,'G');
}

function drawIcons(boy_r,girl_r,blore_boy_r,blore_girl_r,gphpos,gender)
{
   var imghtml = '<div style="width:200px;text-align:center">';
   if(gender == 'G') {
     if (gphpos ==  1) {
       if( parseInt(girl_r) > parseInt(blore_girl_r)) {
         imghtml = imghtml + '<img src="/images/girl_green.png"><br/><b>' + girl_r + '%</b><br/>Girls\' Score';
       } else {
         imghtml = imghtml + '<img src="/images/girl_orange.png"><br/><b>' + girl_r + '%</b><br/>Girls\' Score';
       }
     } else {
       imghtml = imghtml + '<img src="/images/girl_grey.png"><br/><b>' + blore_girl_r + '%</b><br/>Girls\' Score';
     }
   } else {
     if (gphpos ==  1) {
       if( parseInt(boy_r) > parseInt(blore_boy_r)) {
         imghtml = imghtml + '<img src="/images/boy_green.png"><br/><b>' + boy_r + '%</b><br/>Boys\' Score';
       } else {
         imghtml = imghtml + '<img src="/images/boy_orange.png"><br/><b>' + boy_r + '%</b><br/>Boys\' Score';
       }
     } else {
       imghtml = imghtml + '<img src="/images/boy_grey.png"><br/><b>' + blore_boy_r + '%</b><br/>Boys\' Score';
     }
   }
   imghtml = imghtml + '</div>';
   return imghtml;
}


function drawCircle(_cx,_cy,_r,label,color) {
     var circle_txt = '<circle cx="' + _cx + '" cy="' + _cy + '" r="' + logslider(_r) + '" fill="' + color + '"/>';
     var label_txt = '<text x="' + _cx + '" y="' + _cy + '" font-family="sans-serif" font-size="15px" font-weight="bold" text-anchor="middle" fill="black">' + _r + '%</text>';
     var desc_txt = '<text x="' + _cx + '" y="' + (_cy + 100) + '" font-family="sans-serif" font-size="15px" text-anchor="middle" fill="black">' + label + '</text>';
     return circle_txt + label_txt + desc_txt;
}

function libneighbours_chart()
{

}


//UTILITY FUCTIONS----------------------------

function sortDict(unsortedObj)
{
  var sortable = [];
  for (var key in unsortedObj)
  sortable.push([key, unsortedObj[key]]);
  var sortedDict = sortable.sort(function(a, b) {return b[1] - a[1]});
  return sortedDict;
}

function roundPerc(l, target) {
    var off = target - _.reduce(l, function(acc, x) { return acc + Math.round(x) }, 0);
    return _.chain(l).
            //sortBy(function(x) { return Math.round(x) - x }).
            map(function(x, i) { return Math.round(x) + (off > i) - (i >= (l.length + off)) }).
            value();
}

function roundNumber(rnum, rlength) { // Arguments: number to round, number of decimal places
  var newnumber = Math.round(rnum*Math.pow(10,rlength))/Math.pow(10,rlength);
  return parseFloat(newnumber); // Output the result to the form field (change for your purposes)
}


function isEmpty(ob){
  for(var i in ob){ return false;}
  return true;
}

function ConvertToIndian(inputString,colour_code) { 
      cc_str = '';
      if( inputString == undefined || inputString == null)
        inputString = '0'
      if(colour_code){
        val = parseFloat(inputString[0]);
        bm = parseFloat(inputString[1]);
        /*if (val >= bm) {*/
        if (val >= 70) {
          cc_str = '<span style="color:#666;font-size:12pt;font-weight:bold"><span style="color:#43AD2C;">' 
        }
        else {
          cc_str = '<span style="color:#666;font-size:12pt;font-weight:bold"><span style="color:#CD4306;">' 
        }
      }
      inputString = inputString.toString(); 
      var numberArray = inputString.split('.', 2); 
      var pref = parseInt(numberArray[0]); 
      var suf = numberArray[1]; 
      var outputString = ''; 
      if (isNaN(pref)) return ''; 
      var minus = ''; 
      if (pref < 0) minus = '-'; 
      pref = Math.abs(pref).toString(); 
      if (pref.length > 3) { 
      var lastThree = pref.substr(pref.length - 3, pref.length); 
      pref = pref.substr(0, pref.length - 3); 
      if (pref.length % 2 > 0) { 
      outputString += pref.substr(0, 1) + ','; 
      pref = pref.substr(1, pref.length - 1); 
      } 

      while (pref.length >= 2) { 
      outputString += pref.substr(0, 2) + ','; 
      pref = pref.substr(2, pref.length); 
      } 

      outputString += lastThree; 
      } else { 

      outputString = minus + pref; 
      } 

      if (!isNaN(suf)) outputString += '.' + suf; 
      if(colour_code) {
        outputString = cc_str + outputString + '</span>%' 
        outputString = outputString + '<span style="font-size:8pt">&nbsp;&nbsp;&nbsp;' + translations['Bangalore Avg'] + ': ' + bm + '%</span></span>';
        return outputString; 
      } else {
        return outputString; 
      }
}

function ColourIcon(value,key) { 

      val = parseFloat(value[0]);
      /*bm = parseFloat(value[1]);
      if (val >= bm) {*/
      if (val >= 70) {
        return key;
      }
      else {
        return key.replace('.png','n.png');
      }
}
