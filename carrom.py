import math,pygame,time,random
class ball:
    
    def __init__(self,pos,vel,rad,col,den):
        self.pos=pos
        self.vel=vel
        self.rad=rad
        self.col=col
        self.den=den
        
        
def collide_wall(l,b):
    if l[1]!=0:
        theta=math.atan(-l[0]/l[1])
    else:
        theta=1.57079632679
    if b.vel[0]!=0:
        theta1=theta-math.atan(b.vel[1]/b.vel[0])
    else:
        theta1=theta-1.57079632679
    
    ct=math.cos(theta)
    st=math.sin(theta)
    ct1=math.cos(theta1)
    st1=math.sin(theta1)
    
    vpar=b.vel[0]*ct-b.vel[1]*st
    vper=-b.vel[0]*st-b.vel[1]*ct
    
    return (vper*st+vpar*ct,vper*ct-vpar*st)
    
def collide_balls(ball1,ball2,e):
    if ball2.pos[0]-ball1.pos[0] == 0:
        theta=1.57079632679
    else:
        theta=math.atan((ball2.pos[1]-ball1.pos[1])/(ball2.pos[0]-ball1.pos[0]))
    #print(theta)
    m1=ball1.den*ball1.rad**2
    m2=ball2.den*ball2.rad**2
    
    st=math.sin(theta)
    ct=math.cos(theta)
    
    vpar1=ball1.vel[1]*ct - ball1.vel[0]*st
    vpar2=ball2.vel[1]*ct - ball2.vel[0]*st
    
    vrel= (ball1.vel[0]-ball2.vel[0])*ct + (ball1.vel[1]-ball2.vel[1])*st
    
    vper1=(m1*(ball1.vel[0]*ct + ball1.vel[1]*st )+ m2*(ball2.vel[0]*ct + ball2.vel[1]*st - e*vrel))/(m1+m2)
    
    vper2=vper1+e*vrel
    
    
    return ((vper1*ct - vpar1*st , vper1*st + vpar1*ct ), (vper2*ct - vpar2*st , vper2*st + vpar2*ct))


def draw_ball(board,b):
    
    pygame.draw.circle(board,b.col,(int(b.pos[0]),int(b.pos[1])),b.rad)
    

def overlap_ball_wall(b,l):
    if abs((l[0]*b.pos[0] + l[1]*b.pos[1] + l[2])/(l[0]**2+l[1]**2)**.5) <=b.rad:
        return True
    return False
    
def overlap(b,i,j):
    if ((b[i].pos[0]-b[j].pos[0])**2+(b[i].pos[1]-b[j].pos[1])**2)**.5 <= b[i].rad+b[j].rad:
        
        return True
    return False
def check_threat(b):
    ans=[]
    for i in range(len(b)):
        for j in range(i+1,len(b)):
            if overlap(b,i,j)==True:
                ans.append((i,j))
    return ans

def cartesian(r,t):
    t*=1.57079632679/90
    return (width/2-2+r*math.sin(t),height/2-6-r*math.cos(t))     #error correction -6


def game_stop(b):
    if [b[i].vel for i in range(len(b))]==[(0,0)]*len(b):
        return True
    return False

def fix_ball_stuck(b,i):
    
    
    for j in range(len(b)):
        if j!=i:
            val=-((b[i].pos[0]-b[j].pos[0])**2+(b[i].pos[1]-b[j].pos[1])**2)**.5 + b[i].rad+b[j].rad
            if val>0:
                theta=math.atan((b[i].pos[1]-b[j].pos[1])/(b[i].pos[0]-b[j].pos[0]))
                ct=abs(math.cos(theta))
                st=abs(math.sin(theta))
                xf=-1
                yf=-1
                if b[i].pos[0]>b[j].pos[0]:
                    xf=1
                if b[i].pos[1]>b[j].pos[1]:
                    yf=1

                b[i].pos=(b[i].pos[0]+val*ct/2*xf,b[i].pos[1]+val*st/2*yf)
                b[j].pos=(b[j].pos[0]-val*ct/2*xf,b[j].pos[1]-val*st/2*yf)




def check_hole(b,hole,hole_rad,hole_vel):
    #print(hole)
    #print(hole[0])
    #print(hole[1][1])
    holed=[]
    i=len(b)-1
    #print(hole)
    while i>=0:
        for j in range(len(hole)):
            if ((b[i].pos[0]-hole[j][0])**2+(b[i].pos[1]-hole[j][1])**2)**.5 < hole_rad and b[i].vel[0]**2+b[i].vel[1]**2<=hole_vel**2:
                holed.append(b[i])
                b.pop(i)
                i-=1
        i-=1
    return holed




def flip_balls(b,flip):
    for i in range(len(b)):
        temp=list(b[i].pos)
        temp[0]=1000-temp[0]
        temp[1]=1000-temp[1]
        b[i].pos=tuple(temp)
    if flip==1:
        return 0
    return 1

def play_turn(b,board,carrom_board):
    shot_selected=False
    while True:
        for event in pygame.event.get():
            if event.type==pygame.MOUSEMOTION:
                
                board.blit(carrom_board,(0,0))
                for i in b:
                    pygame.draw.circle(board,i.col,(int(i.pos[0]),int(i.pos[1])),i.rad)
                mouse_coord=event.pos
                
                if shot_selected==False:
                    pygame.draw.line(board,pygame.Color(255,255,255),b[0].pos,mouse_coord)
                    
                    
                elif mouse_coord[1]<=400:
                    pygame.draw.rect(board,pygame.Color(0,255,0),(0,mouse_coord[1],100,400-mouse_coord[1]))
                    pygame.draw.line(board,pygame.Color(255,255,255),b[0].pos,final_coord)
                    pygame.draw.rect(board,pygame.Color(115,155,225),(0,0,100,400),3)
                    
                else:
                    pygame.draw.line(board,pygame.Color(255,255,255),b[0].pos,final_coord)
                    pygame.draw.rect(board,pygame.Color(115,155,225),(0,0,100,400),3)
                pygame.display.update()
            elif event.type==pygame.MOUSEBUTTONUP:
                if shot_selected==False:
                    final_coord=event.pos
                    pygame.draw.rect(board,pygame.Color(115,155,225),(0,0,100,400),3)
                    pygame.display.update()
                    shot_selected=True
                else:
                    shot_power=event.pos[1]
                    
                    return [final_coord,shot_power]
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit()




def check_won(b):
    if b[1].col!=pygame.Color(255,0,0):
        check=b[1].col
        for i in range(2,len(b)):
            if b[i].col!=check:
                return False
        return True
    else:
        check=b[2].col
        for i in range(3,len(b)):
            if b[i].col!=check:
                return False
        return True


if __name__=='__main__':
    
    
    pygame.init()
    height=1000
    width=1000
    board=pygame.display.set_mode((width,height))
    frame_per_second=50
    pygame.time.Clock().tick(frame_per_second)
    
    carrom_board=[pygame.transform.scale(pygame.image.load("carrom_board.jpg"),(width,height)),pygame.transform.rotate(pygame.transform.scale(pygame.image.load("carrom_board.jpg"),(width,height)),180)]
    red=pygame.Color(255,0,0)
    white=pygame.Color(255,255,255)
    white1=pygame.Color(0,0,255)
    
    flip=0
    e=1
    friction=50
    holed=[]
    queen=False
     
    r=20                                              #
    R=30                                               #
    holes=[[(35,46),(960,46),(960,947),(35,947)],[(965,954),(40,954),(40,53),(965,53)]]         #
    hole_rad=31.5                                        #
    hole_vel=200                                          #
    shot_line_miny=[836-R,847-R]                                   #for height and width=1000
    shot_line_maxy=[800+R,814+R]                                  #
    shot_line_minx=[227-R,225-R]                                 #
    shot_line_maxx=[771+R,772+R]                                #
    max_vel=500
    
    inipos=[[cartesian(2*r+2,t) for t in [15,135,255]]+[cartesian(4*r+4,t) for t in range(15,345,60)],[cartesian(2*r+2,t) for t in [75,195,315]]+[cartesian(2*(3**0.5)*r+4,t) for t in range(-15,315,60)]]
    
   
    
    
    balls=[ball((165,165),(0,0),R,red,1.5),ball(cartesian(0,0),(0,0),r,red,1)] + [ball(i,(0,0),r,white,1) for i in inipos[0]] + [ball(i,(0,0),r,white1,1) for i in inipos[1]]
    walls=[[1,0,-995],[1,0,-9],[0,1,-983],[0,1,-16]]
    
    while not check_won(balls):
        
        board.blit(carrom_board[flip],(0,0))
        #print(balls[0].vel)
        for i in range(len(balls)):
            
            if balls[i].vel[0]!=0:
                theta=math.atan(balls[i].vel[1]/balls[i].vel[0])
            else:
                theta=1.57079632679
            st=abs(math.sin(theta))
            ct=math.cos(theta)
            
            
            if abs(balls[i].vel[0])>friction/frame_per_second:
                balls[i].vel=(balls[i].vel[0]-abs(balls[i].vel[0])/balls[i].vel[0]*friction/frame_per_second*ct, balls[i].vel[1])
            else:
                balls[i].vel=(0,balls[i].vel[1])
            
            
            if abs(balls[i].vel[1])>friction/frame_per_second:
                balls[i].vel=(balls[i].vel[0] , balls[i].vel[1]-abs(balls[i].vel[1])/balls[i].vel[1]*friction/frame_per_second*st)
            else:
                balls[i].vel=(balls[i].vel[0],0)
        
                
            balls[i].pos=(balls[i].pos[0]+balls[i].vel[0]/frame_per_second,balls[i].pos[1]+balls[i].vel[1]/frame_per_second)
            fix_ball_stuck(balls,i)
            draw_ball(board,balls[i])
#            time.sleep(2)
            #print('ball',i,balls[i].pos,'\t',balls[i].vel,'\n')
        #print(balls[0].vel)
        pygame.display.update()
        if check_threat(balls)!=[]:
            for i in check_threat(balls):
                new_vel=collide_balls(balls[i[0]],balls[i[1]],e)
                #print(new_vel)
                balls[i[0]].vel=new_vel[0]
                balls[i[1]].vel=new_vel[1]
        for i in range(len(balls)):
            for j in range(len(walls)):
                if overlap_ball_wall(balls[i],walls[j])==True:
                    #print('yes',balls[i].pos,balls[i].rad,walls[j])
                    new_vel=collide_wall(walls[j],balls[i])
                    balls[i].vel=new_vel
            
        #print()
        holed.append(check_hole(balls,holes[flip],hole_rad,hole_vel))
  
        
        for event in pygame.event.get():
           if event.type==pygame.KEYDOWN:
            
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit()
        
        if game_stop(balls)==True:
            
            scored=False
            for i in holed:
                for j in i:
                    if j.col==white and flip==0:
                        scored=True
                        if queen==True:
                            queen=-1
                    elif j.col==white1 and flip==1:
                        scored=True
                        if queen==True:
                            queen=-2
                    elif queen==True:
                        balls.insert(1,ball(cartesian(0,0),(0,0),r,red,1))
                        queen=False
                    if j.col==red:
                        queen=True
                        scored=True
            holed=[]
            if scored==False:
                flip=flip_balls(balls,flip)
                board.blit(carrom_board[flip],(0,0))
                for i in balls:
                    draw_ball(board,i)
                pygame.display.update()
            
        
        while game_stop(balls)==True:
            
            
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
            
                    if event.key==pygame.K_q:
                        pygame.quit()
                        quit()
            
                    elif event.key==pygame.K_RIGHT:
                        if balls[0].pos[0]+1<=shot_line_maxx[flip]:
                            balls[0].pos=(balls[0].pos[0]+1,balls[0].pos[1])
                            board.blit(carrom_board[flip],(0,0))
                            for i in range(len(balls)):
                                draw_ball(board,balls[i])
                                if i!=0:
                                    if overlap(balls,0,i)==True:
                                        print("foul")
                            pygame.display.update()


                    elif event.key==pygame.K_LEFT:
                        if balls[0].pos[0]-1>=shot_line_minx[flip]:
                            balls[0].pos=(balls[0].pos[0]-1,balls[0].pos[1])
                            board.blit(carrom_board[flip],(0,0))
                            for i in range(len(balls)):
                                draw_ball(board,balls[i])
                                if i!=0:
                                    if overlap(balls,0,i)==True:
                                        print("foul")
                            pygame.display.update()


                    elif event.key==pygame.K_UP:
                        if balls[0].pos[1]-1>=shot_line_miny[flip]:
                            balls[0].pos=(balls[0].pos[0],balls[0].pos[1]-1)
                            board.blit(carrom_board[flip],(0,0))
                            for i in range(len(balls)):
                                draw_ball(board,balls[i])
                                if i!=0:
                                    if overlap(balls,0,i)==True:
                                        print("foul")
                            pygame.display.update()


                    elif event.key==pygame.K_DOWN:
                        if balls[0].pos[1]+1<=shot_line_maxy[flip]:
                            balls[0].pos=(balls[0].pos[0],balls[0].pos[1]+1)
                            board.blit(carrom_board[flip],(0,0))
                            for i in range(len(balls)):
                                draw_ball(board,balls[i])
                                if i!=0:
                                    if overlap(balls,0,i)==True:
                                        print("foul")
                            pygame.display.update()
                            
                    elif event.key==pygame.K_RETURN:
                        shot_point,shot_power=play_turn(balls,board,carrom_board[flip])
                        theta=math.atan((shot_point[1]-balls[0].pos[1])/(shot_point[0]-balls[0].pos[0]))
                        if shot_point[0]>balls[0].pos[0]:
                            ct=math.cos(theta)
                        else:
                            ct=-math.cos(theta)
                        
                        if shot_point[1]>balls[0].pos[1]:
                            st=abs(math.sin(theta))
                        else:
                            st=-abs(math.sin(theta))
                            
                        balls[0].vel=(max_vel*(400-shot_power)/400*ct , max_vel*(400-shot_power)/400*st)

                elif event.type==pygame.MOUSEBUTTONUP:
                    striker_coord=event.pos
                    #print(striker_coord)
                    if striker_coord[1]>=shot_line_miny[flip] and striker_coord[1]<=shot_line_maxy[flip] and striker_coord[0]>=shot_line_minx[flip] and striker_coord[0]<=shot_line_maxx[flip]:
                        balls[0].pos=striker_coord
                        board.blit(carrom_board[flip],(0,0))
                        for i in range(len(balls)):
                            draw_ball(board,balls[i])
                            if i!=0:
                                if overlap(balls,0,i)==True:
                                    print("foul")
                        pygame.display.update()


    
    
    if balls[1].col==white:
        print('player 2 wins by ',end='')
        if queen==-2:
            print(len(balls)+2,'points')
        else:
            print(len(balls)-1,'points')
    elif balls[1].col==white1:
        print('player 1 wins by ',end='')
        if queen==-1:
            print(len(balls)+1,'points')
        else:
            print(len(balls)-1,'points')
    else:
        if balls[2].col==white:
            print('player 1 wins by',len(balls)+1,'points')
        else:
            print('player 2 wins by',len(balls)+1,'points')
    time.sleep(5)
    pygame.quit()
    
    