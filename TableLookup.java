

class TableLookup {

    double[] x;
    double[] y;

    TableLookup (double[] inputs, double[] outputs) {
        x = inputs;
        y = outputs;
    }

    public double getValue (double input) {

        double x1 = 0, x2 = 0;
        double y1 = 0, y2 = 0;

        for (int i = 0; i < x.length; i++) {
            if (x[i] == input) {
                return y[i];
            }
            if(input > x[i] && input < x[i+1]) {
                x1 = x[i];
                x2 = x[i+1];
                y1 = y[i];
                y2 = y[i+1];
            }
        }

        return y1 + ((input - x1) * ((y2 - y1)/(x2 - x1)));
    }

}