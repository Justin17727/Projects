import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
class Calculator implements ActionListener{
    boolean remove = false;
    String str = "";
    JFrame frame = new JFrame();
    JPanel panel = new JPanel();
    JTextField field = new JTextField();
    JButton numButton[] = new JButton[10];
    JButton opButton[] = new JButton[6];
    Calculator(){
        frame.setTitle("Simple Calculator");
        frame.setResizable(false);
        panel.setLayout(new GridLayout(4, 4, 4, 4));
        frame.getContentPane().setBackground(new Color(254, 215, 191));
        panel.setBackground(new Color(254, 215, 191));
        for(int i = 0; i < 10; i++){
            numButton[i] = new JButton(String.valueOf(i));
            numButton[i].setFont(new Font("Arial", Font.PLAIN, 20));
            numButton[i].setFocusable(false);
            numButton[i].addActionListener(this);
            numButton[i].setBackground(new Color(228, 175, 176));
            numButton[i].setForeground(new Color(154, 119, 135));
        }
        opButton[0] = new JButton("+");
        opButton[1] = new JButton("-");
        opButton[2] = new JButton("\u00d7");
        opButton[3] = new JButton("\u00f7");
        opButton[4] = new JButton("DEL");
        opButton[5] = new JButton("=");
        for(int i = 0; i < 6; i++){
            opButton[i].setFocusable(false);
            opButton[i].setFont(new Font("Arial", Font.PLAIN, 20));
            opButton[i].addActionListener(this);
            opButton[i].setBackground(new Color(228, 175, 176));
            opButton[i].setForeground(new Color(154, 119, 135));
        }
        field.setFont(new Font("Arial", Font.PLAIN, 40));
        field.setEditable(false);
        field.setFocusable(false);
        field.setBounds(25, 30, 335, 80);
        field.setForeground(new Color(154, 119, 135));
        panel.setBounds(25, 120, 335, 400);
        panel.add(numButton[9]);
        panel.add(numButton[8]);
        panel.add(numButton[7]);
        panel.add(opButton[0]);
        panel.add(numButton[6]);
        panel.add(numButton[5]);
        panel.add(numButton[4]);
        panel.add(opButton[1]);
        panel.add(numButton[3]);
        panel.add(numButton[2]);
        panel.add(numButton[1]);
        panel.add(opButton[2]);
        panel.add(opButton[4]);
        panel.add(numButton[0]);
        panel.add(opButton[5]);
        panel.add(opButton[3]);
        frame.add(panel);
        frame.add(field);
        frame.setBounds(400, 50, 400, 600);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(null);
        frame.setVisible(true);
    }
    public static void main(String[] args){
        new Calculator();
    }
    @Override
    public void actionPerformed(ActionEvent e){
        if(remove){
            remove = false;
            field.setForeground(new Color(154, 119, 135));
            field.setFont(new Font("Arial", Font.PLAIN, 40));
            field.setText("");
        }
        for(int i = 0; i < 10; i++){
            if(e.getSource() == numButton[i]){
                field.setText(field.getText()+numButton[i].getText());
            }
        }
        for(int i = 0; i < 4; i++){
            if(e.getSource() == opButton[i]){
                if(field.getText().length() == 0){
                    return;
                }
                for(int j=0; j < 4; j++){
                    if(field.getText().endsWith(opButton[j].getText()) && e.getSource() == opButton[1]){
                        if(field.getText().endsWith(opButton[1].getText()) || field.getText().endsWith(opButton[0].getText())){
                            field.setText(field.getText().substring(0, field.getText().length()-1));
                            field.setText(field.getText() + opButton[i].getText());
                            return;
                        }
                        else{
                            field.setText(field.getText() + opButton[i].getText());
                            return;
                        }
                    }
                }
                for(int j=0; j < 4; j++){
                    if(field.getText().endsWith(opButton[j].getText())){
                        field.setText(field.getText().substring(0, field.getText().length()-1));
                    }
                }
                field.setText(field.getText() + opButton[i].getText());
            }
        }
        if(e.getSource() == opButton[4]){
            for(int i = 0; i < field.getText().length()-1; i++){
                str=str+String.valueOf(field.getText().charAt(i));
            }
            field.setText(str);
            str = "";
        }
        if(e.getSource() == opButton[5]){
            if(field.getText().length() == 0){
                remove = true;
                field.setForeground(Color.RED);
                field.setFont(new Font("Araial", Font.PLAIN, 30));
                field.setText("Enter An Expression!");
                return;
            }
            Postfix p = new Postfix(field.getText());
            remove = p.status;
            if(remove){
                field.setForeground(Color.RED);
                field.setFont(new Font("Arial", Font.PLAIN, 30));
                field.setText("Cannot Divide By 0!");
            }
            else{
                field.setText(String.valueOf(p.result));
            }
        }
    }
}