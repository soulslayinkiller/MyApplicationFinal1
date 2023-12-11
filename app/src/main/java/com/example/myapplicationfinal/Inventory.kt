package com.example.myapplicationfinal

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.TextView

class Inventory : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_inventory)
        val Intent3 = Intent(this, Inventory::class.java)

        val secondActButton11 = findViewById<Button>(R.id.button4)
        secondActButton11.setOnClickListener {
            watchleft = watchleft + 1
            startActivity(Intent3)
        }
        val secondActButton = findViewById<Button>(R.id.button41)
        secondActButton.setOnClickListener {
            watchleft = watchleft - 1
            startActivity(Intent3)
        }
        val secondActButton1 = findViewById<Button>(R.id.button5)
        secondActButton1.setOnClickListener {
            phoneleft = phoneleft + 1
            startActivity(Intent3)
        }
        val secondActButton01 = findViewById<Button>(R.id.button51)
        secondActButton01.setOnClickListener {
            phoneleft = phoneleft - 1
            startActivity(Intent3)
        }
        val secondActButton2 = findViewById<Button>(R.id.button6)
        secondActButton2.setOnClickListener {
            bikeleft = bikeleft + 1
            startActivity(Intent3)
        }
        val secondActButton21 = findViewById<Button>(R.id.button61)
        secondActButton21.setOnClickListener {
            bikeleft = bikeleft - 1
            startActivity(Intent3)
        }
        val secondActButton4 = findViewById<Button>(R.id.button7)
        secondActButton4.setOnClickListener {
            treeleft = treeleft + 1
            startActivity(Intent3)
        }
        val secondActButton41 = findViewById<Button>(R.id.button71)
        secondActButton41.setOnClickListener {
            treeleft = treeleft - 1
            startActivity(Intent3)
        }
        val secondActButton5 = findViewById<Button>(R.id.button8)
        secondActButton5.setOnClickListener {
            gameleft = gameleft + 1
            startActivity(Intent3)
        }
        val secondActButton51 = findViewById<Button>(R.id.button81)
        secondActButton51.setOnClickListener {
            gameleft = gameleft - 1
            startActivity(Intent3)
        }
        val secondActButton3 = findViewById<Button>(R.id.button3)
        secondActButton3.setOnClickListener {
            clipleft = clipleft + 1
            startActivity(Intent3)
        }
        val secondActButton31 = findViewById<Button>(R.id.button31)
        secondActButton31.setOnClickListener {
            clipleft = clipleft - 1
            startActivity(Intent3)
        }

        (findViewById<View>(R.id.textView4) as TextView).text = watchleft.toString() + " Watches are Currently Left in the Inventory "
        (findViewById<View>(R.id.textView3) as TextView).text = phoneleft.toString() + " Iphone 15 Pro's are Currently Left in the Inventory "
        (findViewById<View>(R.id.textView6) as TextView).text = gameleft.toString() + " Playstation 5 Pro Consoles are Currently Left in the Inventory "
        (findViewById<View>(R.id.textView5) as TextView).text = clipleft.toString() + " PaperClips are Currently Left in the Inventory "
        (findViewById<View>(R.id.textView7) as TextView).text = treeleft.toString() + " ChristmasTrees are Currently Left in the Inventory "
        (findViewById<View>(R.id.textView8) as TextView).text = bikeleft.toString() + " Bikes are Currently Left in the Inventory "

        val secondActButton22 = findViewById<Button>(R.id.imageButton1)
        secondActButton22.setOnClickListener {
            val Intent12 = Intent(this, Users::class.java)
            startActivity(Intent12)
        }
    }
}