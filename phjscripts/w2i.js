var page = require('webpage').create();
var output, address;

if(phantom.args.length < 2){
	console.log('Usage: w2i.js <url> <output>');
	phantom.exit();
}
else{
	address = phantom.args[0];
	output = phantom.args[1];
	//page.viewportSize = {width: 550, height: 850};
	//page.zoomFactor = 1.5;
	page.paperSize = { format: 'A4', orientation: 'portrait',  margin: {left: '1cm', right: '1cm', top: '.5cm', bottom: '.5cm'}};
	page.open(address, function(status){
		if(status !== 'success'){
			console.log('Error in loading the given url!');
			phantom.exit();
		}
		else{
			window.setTimeout(function(){
				page.evaluate(function(){
					document.body.bgColor = 'white';
					document.body.style.fontSize = '103%'
				});
				page.render(output);
				phantom.exit();				
			}, 500);
		}
	});
}

