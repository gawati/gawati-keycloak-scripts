var fs = require('fs');
const args = require('yargs').argv;

if(args.new_realm_name==undefined){
	console.log('new_realm_name is not Present in verbose.');
	return;
}

if(args.input_realm==undefined){
	console.log('input_realm is not Present in verbose.');
	return;
}
if(args.output_file==undefined){
	console.log('output_file is not Present in verbose.');
	return;
}   


var fileName = './'+ args.input_realm;

try{
	var file = require(fileName);
}catch (e) {
	console.log('input file is not present');
	return;
}

var clientName = args.new_realm_name;

var UId = generateUId();

changeRealm();
changeRolesRealm();
changeRolesClient();
changeClients();
changeComponents();
changeAuthenticationFlows();
changeAuthenticatorConfig();




fs.writeFile(args.output_file, JSON.stringify(file, null, 2), function (err) {
  if (err) return console.log(err);
  console.log(JSON.stringify(file));
  console.log('writing to ' + args.output_file);
})


function changeRealm(){
	file.id = clientName;
	file.realm = clientName;
}

function changeRolesRealm(){
	if(file.roles.realm!=undefined){
		for(var i =0; i<file.roles.realm.length; i++){
			file.roles.realm[i].id = newName(file.roles.realm[i].id);
		}
	}
}

function changeRolesClient(){
	if(file.roles.client!=undefined){
		for(var c in file.roles.client){
			for(j=0;j< file.roles.client[c].length; j++){
				file.roles.client[c][j].id = newName(file.roles.client[c][j].id);
				file.roles.client[c][j].containerId = newName(file.roles.client[c][j].containerId);
			}
		}
	}
}

function changeClients(){
	if(file.clients!=undefined){
		for(i=0;i< file.clients.length; i++){
			file.clients[i].id = newName(file.clients[i].id);
			
			if(file.clients[i].protocolMappers!=undefined){
				for(j=0;j<file.clients[i].protocolMappers.length;j++){
					file.clients[i].protocolMappers[j].id = newName(file.clients[i].protocolMappers[j].id);
				}
			}

			if(file.clients[i].authorizationSettings!=undefined && file.clients[i].authorizationSettings.resources!=undefined){
				for(j=0;j<file.clients[i].authorizationSettings.resources.length;j++){
					file.clients[i].authorizationSettings.resources[j].name = newName(file.clients[i].authorizationSettings.resources[j].name);
				}
			}

			if(file.clients[i].authorizationSettings!=undefined && file.clients[i].authorizationSettings.policies!=undefined){
				for(j=0;j<file.clients[i].authorizationSettings.policies.length;j++){
					if(file.clients[i].authorizationSettings.policies[j].name!=undefined){
						file.clients[i].authorizationSettings.policies[j].name = newName(file.clients[i].authorizationSettings.policies[j].name);
					}
					if(file.clients[i].authorizationSettings.policies[j].config.resources!=undefined){
						file.clients[i].authorizationSettings.policies[j].config.resources = newName(file.clients[i].authorizationSettings.policies[j].config.resources);
					}
				}
			}
		}
	}
}

function changeComponents(){
	if(file.components!=undefined){
		for(var c in file.components){
			for(j=0;j< file.components[c].length; j++){
				file.components[c][j].id = newName(file.components[c][j].id);
			}
		}
	}
}

function changeAuthenticationFlows(){
	if(file.authenticationFlows!=undefined){
		for(i=0;i< file.authenticationFlows.length; i++){
			file.authenticationFlows[i].id = newName(file.authenticationFlows[i].id);
		}
	}
}

function changeAuthenticatorConfig(){
	if(file.authenticatorConfig!=undefined){
		for(i=0;i< file.authenticatorConfig.length; i++){
			file.authenticatorConfig[i].id = newName(file.authenticatorConfig[i].id);
		}
	}
}

function newName(oldName){
	var position = getPosition(oldName,'-', 3);
	var count = (oldName.match(/-/g) || []).length;
	if(count==4){
		oldName = replaceAt(oldName, position+1,UId);
	}
	return oldName;
}

function generateUId(){
	return randomStringBasedOnName() + '-' + randomString(12);
}

function randomStringBasedOnName(){
	var client = clientName.replace(/\W/g, '').toLowerCase().substring(0, 4);
	for(var i=client.length; i<4;i++){
	 	client = client + i;
	}
	return client;
}

function randomString(length) {
    var result = '';
    chars = '0123456789abcdefghijklmnopqrstuvwxyz';
    for (var i = length; i > 0; --i) result += chars[Math.floor(Math.random() * chars.length)];
    return result;
}


function getPosition(string, subString, index) {
   return string.split(subString, index).join(subString).length;
}

function replaceAt(str, index, replacement) {
    return str.substr(0, index) + replacement+ str.substr(index + replacement.length);
}