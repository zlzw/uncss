var page = require('webpage').create();

page.open(phantom.args[0], function () {
    console.log(page.content);
    phantom.exit();
});