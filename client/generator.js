function generateBlock() {
	var block = new Array();

	//create an array with width and height 8 (the maximum dimensions a block can be)
	for(x = 0; x < 8; x++) {
		block[x] = new Array();
		for(y = 0; y < 8; y++) {
			block[x][y] = false;
		}
	}

	//initial bock at center
	block[4][4] = true;

	//loop find first block then add adjacent blocks
	blocksAdded = 0;
	generated = false;
	while(true){
		if(generated){
			break;
		}
		for(x = 0; x < 8; x++) {
			if(generated){
				break;
			}
			for(y = 0; y < 8; y++) {
				if(generated){
					break;
				}
				if (block[x][y] == true) {
					//direction of new block in relation to current block chose by random number
					direction = Math.floor((Math.random()*4)+0);

					switch(direction) {
					case 0:
						//in case the block is at the edge or already filled
						if(y - 1 < 0 || block[x][y - 1] == true){
							break;
						}
						
						block[x][y - 1] = true;
						blocksAdded++;
						break;
					case 1:
						if(x + 1 >= 8 || block[x + 1][y] == true){
							break;
						}
						block[x + 1][y] = true;
						blocksAdded++;
						break;
					case 2:
						if(y + 1 >= 8 || block[x][y + 1] == true){
							break;
						}
						block[x][y + 1] = true;
						blocksAdded++;
						break;
					case 3:
						if(x - 1 < 0 || block[x - 1][y] == true){
							break;
						}
						block[x - 1][y] = true;
						blocksAdded++;
						break;
					default:
					  //well dang...
					  console.log("well dang: " + direction);
					}
					if (blocksAdded > 4 - 1 - 1){
						generated = true;
					}
				}
			}
		}
	}

	//remove black space around shape
	//dimension around octinomal
	minX = 8;
	minY = 8;
	maxX = 0;
	maxY = 0;
	for(x = 0; x < 8; x++) {
		for(y = 0; y < 8; y++) {
			if(block[x][y] == true){
				if(y < minY){
					minY = y;
				}
				if (x < minX){
					minX = x;
				}
				if(x > maxX){
					maxX = x;
				}
				if(y > maxY){
					maxY = y;
				}
			}
		}
	}

	var newblock = new Array();

	//create an array with width and height 8 (the maximum dimensions a block can be)
	for(x = 0; x < 8 - minX - ((8 - minX) - ((maxX + 1) - minX)); x++) {
		newblock[x] = new Array();
		for(y = 0; y < 8 - minY - ((8 - minY) - ((maxY + 1) - minY)); y++) {
			newblock[x][y] = block[x + minX][y + minY];
		}
	}

	return newblock;
}