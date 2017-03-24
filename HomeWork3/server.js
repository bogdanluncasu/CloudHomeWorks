var fs = require('fs'),
    http = require('http'),
    sio = require('socket.io');

var server = http.createServer(function(req, res) {
  res.writeHead(200, { 'Content-type': 'text/html'});
  res.end(fs.readFileSync('./index.html'));
});
server.listen(8000, function() {
  console.log('Server listening at http://localhost:8000/');
});

io = sio.listen(server);

var players=[]

io.sockets.on('connection', function (socket) {
	players.push(socket);
	if(players.length==2){
		player1=players.pop();
		player2=players.pop();
		player1.broadcast.emit('startgame', "FIRST");
		player2.broadcast.emit('startgame', "SECOND");
		playgame(player1,player2,[0,0,0,0,0,0,0,0,0]);

	}
});



var gameover = function(v){
	if(
		(v[0]==v[1]&&v[1]==v[2]&&v[2]==1)
		||(v[3]==v[4]&&v[4]==v[5]&&v[5]==1)
		||(v[6]==v[7]&&v[7]==v[8]&&v[8]==1)
		||(v[0]==v[3]&&v[3]==v[6]&&v[6]==1)
		||(v[1]==v[4]&&v[4]==v[7]&&v[7]==1)
		||(v[2]==v[5]&&v[5]==v[8]&&v[8]==1)
		||(v[0]==v[4]&&v[4]==v[8]&&v[8]==1)
		||(v[2]==v[4]&&v[4]==v[6]&&v[6]==1)){
			return 1;
	}else if(		
		(v[0]==v[1]&&v[1]==v[2]&&v[2]==2)
		||(v[3]==v[4]&&v[4]==v[5]&&v[5]==2)
		||(v[6]==v[7]&&v[7]==v[8]&&v[8]==2)
		||(v[0]==v[3]&&v[3]==v[6]&&v[6]==2)
		||(v[1]==v[4]&&v[4]==v[7]&&v[7]==2)
		||(v[2]==v[5]&&v[5]==v[8]&&v[8]==2)
		||(v[0]==v[4]&&v[4]==v[8]&&v[8]==2)
		||(v[2]==v[4]&&v[4]==v[6]&&v[6]==2)){
			return 2;
	}else if(v[0]!=0&&v[1]!=0&&v[2]!=0&&v[3]!=0&&
				v[4]!=0&&v[5]!=0&&v[6]!=0&&v[7]!=0&&v[8]!=0){
					return 0;
				}
		return 0;
	
}

var playgame = function(player1,player2,v){
	  player1.on('disconnect',function(msg){
		  player2.emit('over', 'You won. Your enemy left the game.');
	  });
	
	  player2.on('disconnect',function(msg){
		  player1.emit('over', 'You won. Your enemy left the game.');
	  });
	
	  player1.on('turn', function (msg) {
		  v[msg]=1;
		  stat=gameover(v);
		  if(stat!=0){
			  switch(stat){
				  case 1:
					player2.emit('turn', msg);
					player1.emit('over',"You won");
					player2.emit('over',"You lost");
					break;
				  case 2:
					player1.emit('turn', msg);
					player2.emit('over',"You won");
					player1.emit('over',"You lost");
					break;
				  case 3:
					player1.emit('over',"Draw");
					player2.emit('over',"Draw");
				  default:
			  }
			  
		  }else{
			player2.emit('turn', msg);
			player1.emit('stay', '');  
		  }

	  });
	  
	  player2.on('turn', function (msg) {
		  v[msg]=2;
		  stat=gameover(v);
		  if(stat!=0){
			  switch(stat){
				  case 1:
					player1.emit('over',"You won");
					player2.emit('over',"You lost");
					break;
				  case 2:
					player2.emit('over',"You won");
					player1.emit('over',"You lost");
					break;
				  default:
					player1.emit('over',"Draw");
					player2.emit('over',"Draw");
			  }
			  
		  }else{
			player1.emit('turn', msg);
			player2.emit('stay', '');  
		  }
	  });
	  
}