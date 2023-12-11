package com.example.myapplicationfinal

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import java.time.LocalDateTime
var timenow = 0
class PurchasePage : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_purchase_page)

        val secondActButton2 = findViewById<Button>(R.id.imageButton1)
        secondActButton2.setOnClickListener {
            val Intent1 = Intent(this, MainActivity2::class.java)
            startActivity(Intent1)
        }

        if (watchcount > 0){
        (findViewById<View>(R.id.textView4) as TextView).text = watchcount.toString() + " Watches "}
        if (gamecount > 0){
        (findViewById<View>(R.id.textView5) as TextView).text = gamecount.toString() + " PlayStations Consoles "}
        if (clipcount > 0){
        (findViewById<View>(R.id.textView6) as TextView).text = clipcount.toString() + " Paper Clips "}
        if (bikecount > 0){
        (findViewById<View>(R.id.textView7) as TextView).text = bikecount.toString() + " Dirt Bikes "}
        if (treecount > 0){
        (findViewById<View>(R.id.textView8) as TextView).text = treecount.toString() + " Christmas Trees "}
        if (phonecount > 0){
        (findViewById<View>(R.id.textView9) as TextView).text = phonecount.toString() + " Phones "}


        val secondActButton = findViewById<Button>(R.id.button)
        secondActButton.setOnClickListener {
            val Intent9 = Intent(this, ThankYou::class.java)
            startActivity(Intent9)
            watchleft = watchleft - watchcount
            phoneleft = phoneleft - phonecount
            treeleft = treeleft - treecount
            clipleft = clipleft - clipcount
            gameleft = gameleft - gamecount
            bikeleft = bikeleft - bikecount
            watchcount = 0
            phonecount = 0
            treecount = 0
            clipcount = 0
            gamecount = 0
            bikecount = 0
            var timenow = LocalDateTime.now()

        }

            val secondActButton5 = findViewById<Button>(R.id.button2)
            secondActButton5.setOnClickListener {
                watchcount = 0
                phonecount = 0
                treecount = 0
                clipcount = 0
                gamecount = 0
                bikecount = 0
                val Intent3 = Intent(this, PurchasePage::class.java)
                startActivity(Intent3)
            }
        val secondActButton51 = findViewById<Button>(R.id.button4)
        secondActButton51.setOnClickListener {
            val Intent31 = Intent(this, MainActivity2::class.java)
            startActivity(Intent31)
        }

        }
        }

