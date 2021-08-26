import pygame
import random
import neat

pygame.init()
gamefont=pygame.font.SysFont('comicsansms',40)


screenwidth=432
screenheight=768

#bird
birdupflap=pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png'))
birdmidflap=pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png'))
birddownflap=pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png'))
birdimgs=[birddownflap,birdmidflap,birdupflap]

#pipe
pipeimg=pygame.image.load('assets/pipe-green.png')
pipeimg=pygame.transform.scale2x(pipeimg)

#background
bg_surface=pygame.image.load('assets/background-day.png')
bg_surface=pygame.transform.scale(bg_surface,(432,768))

#floor
floor=pygame.image.load('assets/base.png')
floor=pygame.transform.scale2x(floor)
floor2=pygame.image.load('assets/base.png')
floor2=pygame.transform.scale2x(floor2)

class Bird:
	imgs=birdimgs
	gravity=0.25
	max_rotation=45
	rot_vel=10
	anim_time=10
	birdmovement=0
	birdindex=0

	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.tilt=0
		self.tickcount=0
		self.vel=0
		self.height=self.y
		self.birdindex=0
		self.img=self.imgs[0]
		self.imgcount=0

	def jump(self):
		self.vel=-10.5
		self.tickcount=0
		self.height=self.y

	def movebird(self):
		self.tickcount+=1
		disp=self.vel*self.tickcount+ 1.5*self.tickcount**2
		if disp>=16:
			disp=16

		if disp<0:
			disp-=2
		self.y+=disp

		if disp<0:
			if self.tilt<self.max_rotation:
				self.tilt+=0.5*self.tickcount

		if disp>0:
			if self.tilt>-45:
				self.tilt-=0.5*self.tickcount

	def drawbird(self,win):
		self.imgcount+=1
		self.img=self.imgs[self.imgcount%3]

		newrect=self.img.get_rect(center=(self.x,self.y))
		rotimg=pygame.transform.rotate(self.img,self.tilt)
		win.blit(rotimg,newrect)

	def get_mask(self):
		return pygame.mask.from_surface(self.img)
	
class Pipe:
	gap=200
	floorvel=10
	pipeheight=[-150,-100,-50,0,100,150,200,250,300,350,400,450,500,550,600]


	def __init__(self):
		self.height=0
		self.bottom=0
		self.top=0
		self.x=700
		self.topimg=pygame.transform.flip(pipeimg,False,True)
		self.botimg=pipeimg 
		self.passed=False
		self.set_height()

	def set_height(self):
		self.height=random.randrange(-50,500)
		self.top=self.height-self.topimg.get_height()
		self.bottom=self.height+self.gap

 
	def movepipe(self):
		self.x-=self.floorvel


	def drawpipe(self,win):
		win.blit(self.topimg,(self.x,self.top))
		win.blit(self.botimg,(self.x,self.bottom))

	def collide(self,bird):
		birdmask=bird.get_mask()
		topmask=pygame.mask.from_surface(self.topimg)
		bottommask=pygame.mask.from_surface(self.botimg)

		topoffset=(int(self.x-bird.x),int(self.top-round(bird.y)))
		bottomoffset=(int(self.x-bird.x),int(self.bottom-round(bird.y)))

		bpoint=birdmask.overlap(bottommask,bottomoffset)
		tpoint=birdmask.overlap(topmask,topoffset)

		if tpoint or bpoint:
			return True

		else:
			return False

class Floor:
	floorvel=10
	width=floor.get_width()

	def __init__(self):
		self.x1=0
		self.x2=self.width

	def movefloor(self):
		self.x1-=self.floorvel
		self.x2-=self.floorvel

		if self.x2<0:
			self.x1=0
			self.x2=self.width

	def drawfloor(self,win):
		win.blit(floor,(self.x1,700))
		win.blit(floor,(self.x2,700))

def drawwindow(win,birds,pipes,floor,score):
	win.blit(bg_surface,(0,0))
	for bird in birds:
		bird.drawbird(win)

	for pipe in pipes:
		pipe.drawpipe(win)

	floor.drawfloor(win)
	scoresurface=gamefont.render(f'Score:{str(score)}',True,(255,255,255))
	#scorerect=scoresurface.get_rect(center=(screenwidth/2))
	win.blit(scoresurface,(250,40))
	pygame.display.update()

def main(genomes,config) :
	run=True
	nets=[]
	ge=[]
	birds=[]
	
	floor=Floor()
	pipes=[Pipe()]
	score=0
	highscore=0


	for _,g in genomes:
		net=neat.nn.FeedForwardNetwork.create (g,config)
		nets.append(net)
		birds.append(Bird(screenwidth/2,screenheight/2))
		g.fitness=0
		ge.append(g)


	
	win=pygame.display.set_mode((screenwidth,screenheight))
	run=True
	clock=pygame.time.Clock()

	while run:
		clock.tick(150)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				run=False
				pygame.quit()
				quit()
				break
	
		pipind=0
		if len(birds)>0:
			if len(pipes)>1 and birds[0].x> pipes[0].x+pipeimg.get_width():
				pipind=1

		else:
			run=False
			break

		for x,bird in enumerate(birds):
			ge[x].fitness+=0.1
			bird.movebird()
			output=nets[x].activate((bird.y,abs(bird.y-pipes[pipind].height),abs(bird.y-pipes[pipind].bottom)))
			
			if output[0]>0.5:
				bird.jump()



		rem=[]
		addpipe=False
		for pipe in pipes:
			pipe.movepipe()
			for i,bird in enumerate(birds):
				if pipe.collide(bird):
					ge[i].fitness-=1
					birds.pop(i)
					nets.pop(i)
					ge.pop(i)
			

			if pipe.x+pipeimg.get_width()<0:
				rem.append(pipe)
			
			if bird.x>pipe.x:
				pipe.passed=True


		if pipe.passed:
			pipes.append(Pipe())
			score+=1
			for g in ge:
				g.fitness+=5

		for r in rem:
			pipes.remove(r)

			for x,bird in enumerate(birds):
				if bird.y+bird.img.get_height()>=800 or bird.y<-100:
					ge[x].fitness-=1
					birds.pop(x)
					nets.pop(x)
					ge.pop(x)
		

			
		floor.movefloor()
		drawwindow(win,birds,pipes,floor,score)

configpath='C:/Users/Mega/Desktop/ML/neatflappyconfig.txt'

def run(configpath):
		config=neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,configpath)
		pop=neat.Population(config)
		pop.add_reporter(neat.StdOutReporter(True))
		stats=neat.StatisticsReporter()
		pop.add_reporter(stats)
		winner=pop.run(main,50)

run(configpath)