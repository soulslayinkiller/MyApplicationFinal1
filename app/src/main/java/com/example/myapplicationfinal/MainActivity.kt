package com.example.myapplicationfinal

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.SystemClock
import android.widget.Button
import java.time.LocalTime

var watchcount = 0
var phonecount = 0
var treecount = 0
var clipcount = 0
var bikecount = 0
var gamecount = 0
var watchlist1 = 76
var gamelist2 = 47
var cliplist3 = 56
var bikelist4 = 8
var treelist5 = 20
var phonelist6 = 582
var watchleft = watchlist1
var gameleft = gamelist2
var clipleft = cliplist3
var bikeleft = bikelist4
var treeleft = treelist5
var phoneleft = phonelist6
val startTime = LocalTime.now()
var timesince = 0




class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val secondActButton = findViewById<Button>(R.id.button1)
        secondActButton.setOnClickListener {
            val Intent = Intent(this, MainActivity2::class.java)
            startActivity(Intent)
        }

        val secondActButton1 = findViewById<Button>(R.id.button2)
        secondActButton1.setOnClickListener {
            val Intent = Intent(this, Users::class.java)
            startActivity(Intent)



        }
    }
}
