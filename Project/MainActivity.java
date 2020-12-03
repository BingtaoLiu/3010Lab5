package com.example.myfirstapp;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private ToggleButton toggleButton;
    private Button closeButton;
    private TextView lightSwitch;
    private TextView tempDisplay;
    private TextView humDisplay;
    private TextView co2Display;
    private TextView methaneDisplay;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        tempDisplay = (TextView)findViewById(R.id.temp);
        humDisplay = (TextView)findViewById(R.id.hum);
        co2Display = (TextView)findViewById(R.id.co2);
        methaneDisplay = (TextView)findViewById(R.id.methane);
        lightSwitch = (TextView)findViewById(R.id.ls) ;

        addListenerOnButtonClick();

    }

    public void addListenerOnButtonClick(){
        //Getting the ToggleButton layout xml file
        toggleButton=(ToggleButton)findViewById(R.id.onOff);
        closeButton = (Button)findViewById(R.id.closeApp);
        lightSwitch = (TextView)findViewById(R.id.ls) ;
        lightSwitch.setText(" ") ;
        //Performing action on button click

        toggleButton.setOnClickListener(new View.OnClickListener(){

        @SuppressLint("SetTextI18n")
        @Override
        public void onClick(View view) {
        //StringBuilder result = new StringBuilder();
       // result.append("Light Switch: ").append(toggleButton.getText());
        //Displaying the message in toast
        //Toast.makeText(getApplicationContext(), result.toString(), Toast.LENGTH_LONG).show();
        System.out.println(toggleButton.getText());

        if(toggleButton.isChecked() == true){
            lightSwitch.setText("Light Switch ON");

        } else if (toggleButton.isChecked() == false) {
            lightSwitch.setText("Light Switch OFF");

        }


        }

        });

        closeButton.setOnClickListener(new View.OnClickListener(){
            @SuppressLint("SetTextI18n")
            @Override
            public void onClick(View view) {
                System.out.println("Button Working");
                //send Disconnet message to server

            }

        });


    }

}


