var year='';
var flag='1';
function displayPane(dat,cons,parent,child)
{
  rep_type=document.getElementById('rep_op').value;
  value=document.getElementById(cons).value;
  year=document.getElementById('year').value;
  if(child!='none'){
      fill_dropdown(dat,child,value);
  }
  if(value=='MLA' || value=='BLOCK' || value=='CLUSTER'){
      value=document.getElementById(parent).value;
      cons=parent;
  }
  clear_dropdown(cons);
  document.getElementById('error_pane').style.visibility="hidden";
  var the_list = dat[cons];
 // for (key in the_list)
   // alert(key);
  heading_str = "<h1>" + cons.toUpperCase() + " Reports " + "</h1>";
  content_str = heading_str + '<div class="div-table">';
  disclaimer_str ='<div id="disclaimer"><b>Disclaimer:</b> These reports below are being furnished for your information. You may choose to reproduce or redistribute this information in part or in full to any other person with due acknowledgement of Karnataka Learning Partnership (KLP). You will ensure that no part of the information provided here may be quoted out of context or misrepresented. KLP makes every effort to use reliable and comprehensive information from the government and other independent sources, but KLP does not represent that the data or information are accurate or complete. KLP is an independent, not-for-profit group. The information provided herein has been provided without regard to the objectives or opinions of those who may receive it. Please also see the <a href="http://www.klp.org.in/text/disclaimer" target="_blank">KLP Data Disclaimer</a>.</div>'
  var rep_types=['Demographics','Finance','Infrastructure','Library','Learning'];
/*  heading_str = "<p class='bordered_text'>" + cons.toUpperCase() + " Reports - " + cons.toTitleCase() + "</p>"; */
 // content_str = disclaimer_str + heading_str + '<div class="div-table">';
  if(rep_type=='dise'){
    rep_types.length=3;
    url_start='/charts/' + cons +'/' + value;
    url_end='/' + year;
  }
  else{
    url_start='http://reports.klp.org.in/charts/' + cons + '/' + value;
    url_end=''
  }
  content_str = '<div class="div-table">';
  for(i=0;i<rep_types.length;i++){
      content_str = content_str +  '<div class="div-table-row">';
      content_str = content_str + '<div class="div-table-col">' + rep_types[i] + '</div>';
      content_str = content_str+'<div class="div-table-col2"><a target="_blank" href="' + url_start + '/english/' + rep_types[i].toLowerCase() + url_end + '"> English</a></div>';
      content_str = content_str+'<div class="div-table-col2"><a target="_blank" href="' + url_start + '/kannada/' + rep_types[i].toLowerCase() + url_end+ '"> Kannada</a></div></div>';
  }
  content_str = content_str +  '</div>';
  var a='<br/>For older PDF reports <a href="http://www.klp.org.in/listFiles/1" target="_blank">click here</a>.';
  document.getElementById('content_pane').innerHTML = content_str;
  if(value=='MP' || value=='DISTRICT')
      document.getElementById('content_pane').innerHTML = '';
}

function showErrorsIfAny(data)
{
  if (data["errormsg"] != undefined)
    document.getElementById('error_pane').style.visibility="visible";
    document.getElementById('error_pane').innerHTML = '<p class="bordered_text"><span style="color:red">' + data["errormsg"] + '</span></p>'; 
}

String.prototype.toTitleCase = function() {
    var aStr = this.split(' ');
    var aProp = [];
    for (str in aStr) {
        aProp.push(aStr[str].charAt(0).toUpperCase() + aStr[str].slice(1));
    }
    return aProp.join(' ');
};

function createOption(dropdown, text, value) {
    var opt = document.createElement('option');
    opt.value = value;
    opt.text = text;
    dropdown.appendChild(opt);
}

function fill_dropdown(data, type, parent, opt){
    if(opt == undefined){
        var opt = document.getElementById('rep_op').value;
    }
    var the_list=data[type][opt];
    if(type!='year')
        document.getElementById(type).length=1;
    for(key in the_list){
        if(the_list[key][2]==parent)
            createOption(document.getElementById(type), the_list[key][1], the_list[key][0]);
    }
}

function initialize_dropdown(data){
    fill_dropdown(data,'mp','1','dise');
    fill_dropdown(data,'district','2','dise');
    fill_dropdown(data,'year','3','dise');
}

function clear_dropdown(type){
    var temp=new Array();
    //document.getElementById('year').length=0;
    if(type=='mp' || type=='mla')
        temp=['district','block','cluster'];
    else if(type=='district')
        temp=['mp','mla','cluster'];
    else if(type=='block')
        temp=['mp','mla'];
    for(i=0;i<temp.length;i++)
        if(i==0)
            document.getElementById(temp[i]).selectedIndex=0;
        else
            document.getElementById(temp[i]).length=1;
}

function replace_year(value){
    //alert(document.getElementById('content_pane').innerHTML.length);
    if(document.getElementById('content_pane').innerHTML.length>1)
    document.getElementById('content_pane').innerHTML=document.getElementById('content_pane').innerHTML.replace(new RegExp(year,'g'),value);
    year=value;
}

function loadData(show,hidden,value){
    flag=value;
    for(var i=0;i<show.length;i++){
        document.getElementById(show[i]+'_div').style.display='block';
/*	else
	    document.getElementById(show[i]+'_div').style.display='none';*/
    }
    for(var i=0;i<hidden.length;i++){
        document.getElementById(hidden[i]+'_div').style.display='none';
    }
}

function change_report(data,value){
    clear_dropdown('mp');
    clear_dropdown('district');
    clear_dropdown('block');
    document.getElementById('year').length=0;
    document.getElementById('content_pane').innerHTML = '';
    if(value=='klp'){
        document.getElementById('year_div').style.display='none';
        document.getElementById('corporator_div').style.display='inline-block';
    }
    else{
        document.getElementById('year_div').style.display='inline-block';
        document.getElementById('corporator_div').style.display='none';
    }
    fill_dropdown(data,'mp','1',value);
    fill_dropdown(data,'district','2',value);
    fill_dropdown(data,'year','3',value);
}
