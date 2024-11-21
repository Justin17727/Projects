import java.awt.*;
import javax.swing.*;
public class Main {
    public static void main(String args[]) throws Exception{
        JFrame frame = new JFrame("Flappy Bird");
        Image icon = new ImageIcon("./FlappyBirdIcon.png").getImage();
        FlappyBird bird = new FlappyBird();
        frame.setSize(360, 500);
        frame.setLocationRelativeTo(null);
        frame.setIconImage(icon);
        frame.setResizable(false);
        frame.add(bird);
        frame.setDefaultCloseOperation(frame.EXIT_ON_CLOSE);
        bird.requestFocus();
        frame.setVisible(true);
        frame.pack();
    }
}
