import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import javax.sound.sampled.*;
import java.io.*;
import java.util.Random;
public class FlappyBird extends JPanel implements ActionListener, KeyListener{
    Image background;
    Image bottomPipe;
    Image topPipe;
    Image birdImg;
    Image ground;
    JLabel Score;
    Pipe topPipes[] = new Pipe[4];
    Pipe bottomPipes[] = new Pipe[4];
    int frameWidth = 360;
    int frameHeight = 500;
    int birdX = frameWidth/8;
    int birdY = frameHeight/2;
    int birdWidth = 42;
    int birdHeight = 38;
    class Bird{
        int x = birdX;
        int y = birdY;
        int width = birdWidth;
        int height = birdHeight;
        Image img;
        Bird(Image p){
            this.img = p;
        }
    }
    class Pipe{
        int x = 500;
        int y = 10;
        int width = 50;
        int height = 500;
        boolean giveScore = true;
        Image img;
        Pipe(Image p){
            this.img = p;
        }
    }
    Bird bird;
    int birdVelUp = 12;
    int birdVelDown = 0;
    int gravity = -1;
    int pipeGapY = 310;
    int pipeGapX = 180;
    int pipeVel = 1;
    Random rand = new Random();
    int randomHeight;
    int score = 0;
    Timer gameLoop;
    boolean gameOver = false;
    private Clip flapSound;
    private Clip hitSound;
    private Clip scoreSound;
    boolean start = false;
    FlappyBird(){
        setPreferredSize(new Dimension(360, 500));
        setFocusable(true);
        addKeyListener(this);
        background = new ImageIcon(getClass().getResource("./FlappyBirdBackground.png")).getImage();
        topPipe = new ImageIcon(getClass().getResource("./FlappyBirdPipe.png")).getImage();
        bottomPipe = new ImageIcon(getClass().getResource("./FlappyBirdPipeB.png")).getImage();
        birdImg = new ImageIcon(getClass().getResource("./FlappyBirdBird.png")).getImage();
        bird = new Bird(birdImg);
        ground = new ImageIcon(getClass().getResource("./FlappyBirdGround.png")).getImage();
        Score= new JLabel(String.valueOf(score));
        for(int i=0; i<4; i++){
            randomHeight = rand.nextInt(300)-150;
            topPipes[i] = new Pipe(bottomPipe);
            topPipes[i].x+=180*i;
            topPipes[i].y=randomHeight;
            topPipes[i].y+=pipeGapY;
            bottomPipes[i] = new Pipe(bottomPipe);
            bottomPipes[i].x+=180*i;
            bottomPipes[i].y=randomHeight;
            bottomPipes[i].y-=pipeGapY;
        }
        flapSound = loadSound("FlappyBirdFlapSound.wav.wav");
        scoreSound = loadSound("FlappyBirdPointSound.wav.wav");
        hitSound = loadSound("FlappyBirdHitSound.wav.wav");
        gameLoop = new Timer(1000/40, this);
    }
    public void paintComponent(Graphics g){
        super.paintComponent(g);
        draw(g);
    }
    public void draw(Graphics g){
        g.drawImage(background, 0, 0, 900, 504, null);
        g.drawImage(birdImg, bird.x, bird.y, birdWidth, birdHeight, null);
        g.drawImage(ground, -20, 460, frameWidth+50, 45, null);
        for(int i=0; i<4; i++){
            g.drawImage(bottomPipe, topPipes[i].x, topPipes[i].y, topPipes[i].width, topPipes[i].height, null);
            g.drawImage(topPipe, bottomPipes[i].x, bottomPipes[i].y, bottomPipes[i].width, bottomPipes[i].height, null);
        }
        g.setFont(new Font("Arial", Font.BOLD, 30));
        g.setColor(Color.WHITE);
        g.drawString(String.valueOf(score), frameWidth/2, 30);
        if(!start){
            g.setFont(new Font("Arial", Font.BOLD, 20));
            g.setColor(Color.ORANGE);
            g.drawString("PRESS SPACEBAR", 80, frameHeight/2);
            g.drawString("TO START", 120, frameHeight/2+50);
        }
        if(gameOver){
            g.setFont(new Font("Arial", Font.BOLD, 50));
            g.setColor(Color.RED);
            g.drawString("GAME OVER", 25, frameHeight/2);
            g.setFont(new Font("Arial", Font.BOLD, 20));
            g.setColor(Color.BLACK);
            g.drawString("PRESS ENTER", 110, frameHeight/2+50);
        }
    }
    public void flap(){
        birdVelDown=birdVelUp;
        playSound(flapSound);
    }
    public void score(Bird bird, Pipe pipe){
        if(bird.x >= pipe.x && pipe.giveScore){
            score++;
            pipe.giveScore=false;
            playSound(scoreSound);
        }
    }
    public boolean collisionWithGround(Bird bird){
        return bird.y < -10 || bird.y > 430;
    }
    public boolean collisionWithPipe(Bird bird, Pipe pipe){
        return  bird.x < pipe.x+pipe.width-10 &&
                bird.x + bird.width-10 > pipe.x &&
                bird.y < pipe.y+pipe.height-15 &&
                bird.y + bird.height-15 > pipe.y;
    }
    public void restart(){
        bird.y = frameHeight/2;
        birdVelDown = 0;
        score = 0;
        for(int i=0; i<4; i++){
            randomHeight = rand.nextInt(300)-150;
            topPipes[i].x=500+180*i;
            topPipes[i].y=randomHeight;
            topPipes[i].y+=pipeGapY;
            topPipes[i].giveScore=true;
            bottomPipes[i].x=500+180*i;
            bottomPipes[i].y=randomHeight;
            bottomPipes[i].y-=pipeGapY;
        }
        gameOver = false;
        gameLoop.start();
    }
    public Clip loadSound(String file){
        try{
            File f = new File(file);
            AudioInputStream a= AudioSystem.getAudioInputStream(f);
            Clip clip = AudioSystem.getClip();
            clip.open(a);
            return clip;
        }catch(Exception e){
            return null;
        }
    }
    public void playSound(Clip clip){
        if(clip != null){
            if(clip.isRunning()){
                clip.stop();
            }
            clip.setFramePosition(0);
            clip.start();
        }
    }
    @Override
    public void actionPerformed(ActionEvent e) {
        birdVelDown+=gravity;
        bird.y-=birdVelDown;
        for(int i=0; i<4; i++){
            if(collisionWithPipe(bird, topPipes[i]) || collisionWithPipe(bird, bottomPipes[i]) || collisionWithGround(bird)){
                gameOver=true;
            }
            score(bird, topPipes[i]);
            if(topPipes[i].x < -300){
                randomHeight = rand.nextInt(300)-150;
                topPipes[i].x=topPipes[(i+3)%4].x + pipeGapX;
                topPipes[i].y=randomHeight+pipeGapY;
                topPipes[i].giveScore=true;
                bottomPipes[i].x=bottomPipes[(i+3)%4].x + pipeGapX;
                bottomPipes[i].y=randomHeight-pipeGapY;
            }
            else{
                topPipes[i].x -= 3;
                bottomPipes[i].x -= 3;
            }
        }
        if(gameOver){
            playSound(hitSound);
            gameLoop.stop();
        }
        repaint();
    }
    @Override
    public void keyTyped(KeyEvent e){}
    @Override
    public void keyPressed(KeyEvent e) {
        if(e.getKeyCode() == KeyEvent.VK_SPACE){
            flap();
        }
        if(e.getKeyCode() == KeyEvent.VK_SPACE && !start){
            flap();
            start = true;
            gameLoop.start();
        }
        if(e.getKeyCode() == KeyEvent.VK_ENTER && gameOver){
            restart();
        }
    }
    @Override
    public void keyReleased(KeyEvent e){}
}