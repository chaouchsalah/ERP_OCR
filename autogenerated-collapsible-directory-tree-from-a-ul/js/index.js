/* Folder Tree */
var foldersList = ['assets',
	['css', 'typography.css', 'layout.css', 'states.css'],
	['js', 'custom.js', 'jquery.js'],
	['images', 'logo.svg', 'arrow-sprite.svg'],
	['test']
];
/*var folders = "<li id='assets'>assets" +
	"<ul><li id='css'>css<ul><li>typography.css</li><li>layout.css</li><li>modules.css</li><li>states.css</li><li>theme.css</li></ul>" +
	"</li>" +
	"<li id='js'>js<ul><li>custom.js</li><li>jquery.js</li></ul></li>" +
	"<li id='images'>images<ul><li>logo.svg</li><li>arrow-sprite.svg</li><li>social-sprite.svg</li></ul></li>" +
	"<li>functions.php</li>" +
	"<li id='test'>Test<ul></ul></li>";*/

function recursiveTree(foldersList) {
	var str = "";
	for (var i = 0; i < foldersList.length; i++) {
		if (i == 0) {
			str += "<li id='" + foldersList[i] + "'>" + foldersList[i] + "<ul>";
		}
		if (typeof (foldersList[i]) == "string" && i != 0) {
			str += "<li id='" + foldersList[i] + "'>" + foldersList[i];
		}
		if (typeof (foldersList[i]) == "string" && typeof (foldersList[i + 1]) != "object" && i != 0) {
			str += "</li>";
		}
		if (typeof (foldersList[i]) == "object") {
			str += recursiveTree(foldersList[i]) + "</ul>";
		}
	}
	str += "</li>";
	return str;
}

var folders = recursiveTree(foldersList);
alert(folders);

function createFolders() {
	$(".directory-list").html(folders);
	var allFolders = $(".directory-list li > ul");
	allFolders.each(function () {
		var folderAndName = $(this).parent();
		folderAndName.addClass("folder");
		var backupOfThisFolder = $(this);
		$(this).remove();
		folderAndName.wrapInner("<a href='#'  class='rightclickarea'/>");
		folderAndName.append(backupOfThisFolder);

		folderAndName.find("a").click(function (e) {
			$(this).siblings("ul").slideToggle("slow");
			e.preventDefault();
		});

	});
}
$(document).ready(function () {
	createFolders();
});
/* Right click */
var current_selected;
$(document).ready(function () {
	$('.rightclickarea').bind('contextmenu', function (e) {
		current_selected = $(this).parent().attr('id');
		var $cmenu = $('.vmenu');
		$('<div class="overlay"></div>').css({
			left: '0px',
			top: '0px',
			position: 'absolute',
			width: '100%',
			height: '100%',
			zIndex: '100'
		}).click(function () {
			$(this).remove();
			$cmenu.hide();
		}).bind('contextmenu', function () {
			return false;
		}).appendTo(document.body);
		$('.vmenu').css({
			left: e.pageX,
			top: e.pageY,
			zIndex: '101'
		}).show();
		return false;
	});

	$('.vmenu .first_li').on('click', function () {
		$('.vmenu').hide();
		$('.overlay').hide();
	});

	$(".first_li").hover(function () {
			$(this).css({
				backgroundColor: '#E0EDFE',
				cursor: 'pointer'
			});
			$(this).css({
				cursor: 'default'
			});
		},
		function () {
			$(this).css('background-color', '#fff');
		});
});

/* New folder */
$("#new_folder").click(function () {
	$('.dialog').html(current_selected);
});