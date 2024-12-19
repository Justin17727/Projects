class Postfix{
    StringBuffer[] postfix;
    int postfixSize;
    double result;
    Postfix(String a){
        infixToPostfix(a);
        postfixEval(this.postfix, this.postfixSize);
    }
    public int priority(char a){
        switch (a){
            case '(':
            case ')':
                return 0;
            case '+':
            case '-':
                return 1;
            case '*':
            case '/':
                return 2;
            case '^':
                return 3;
            default:
                return -1;
        }
    }
    public void infixToPostfix(String str){
        StringBuffer s = new StringBuffer(str);
        StringBuffer[] postfix = new StringBuffer[str.length()];
        for(int i=0; i<str.length(); i++){
            postfix[i] = new StringBuffer("");
        }
        char stack[] = new char[s.length()];
        int top = -1, postTop = -1;
        stack[++top] = '(';
        s.append(")");
        for(int i = 0; i < str.length(); i++){
            if(Character.isDigit(s.charAt(i)) || s.charAt(i) == '.'){
                postTop++;
                while(Character.isDigit(s.charAt(i))){
                    postfix[postTop].append(s.charAt(i));
                    i++;
                }
                i--;
            }
            else if(s.charAt(i) == '('){
                stack[++top] = s.charAt(i);
            }
            else if(s.charAt(i) == ')'){
                while(stack[top] != '('){
                    postfix[++postTop].append(stack[top--]);
                }
                top--;
            }
            else if(priority(s.charAt(i)) > 0){
                while(priority(s.charAt(i)) < priority(stack[top]) || (priority(s.charAt(i)) == priority(stack[top]) && s.charAt(i) != '^')){
                    postfix[++postTop].append(stack[top--]);
                }
                stack[++top] = s.charAt(i);
            }
        }
        while(top != 0){
            postfix[++postTop].append(stack[top--]);
        }
        this.postfix = postfix;
        this.postfixSize = postTop + 1;
        return;
    }
    public void postfixEval(StringBuffer[] s, int size){
        double[] stack = new double[size];
        int top = -1;
        for(int i = 0; i < size; i++){
            try{
                stack[++top] = Double.parseDouble(new String(s[i]));
            }
            catch(NumberFormatException e){
                top--;
                double b = stack[top--];
                double a = stack[top--];
                String symbol = new String(s[i]);
                switch(symbol.charAt(0)){
                    case '+':
                        stack[++top] = a + b;
                        break;
                    case '-':
                        stack[++top] = a - b;
                        break;
                    case '*':
                        stack[++top] = a * b;
                        break;
                    case '/':
                        if(b == 0){
                            System.out.println("Cannot divide by zero!");
                            return;
                        }
                        stack[++top] = a / b;
                        break;
                    //case '^':
                    //    stack[++top] = pow(a, b);
                    //    break;
                    default:
                        System.out.println("Invalid operator: "+ s[i]);
                }
            }
        }
        double result = stack[top];
        this.result = result;
    }
}
