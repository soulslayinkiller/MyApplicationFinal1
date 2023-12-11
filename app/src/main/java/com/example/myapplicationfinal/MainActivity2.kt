package com.example.myapplicationfinal

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity

class MainActivity2 : AppCompatActivity() {
    var count = 0

    @SuppressLint("WrongViewCast")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main2)
        val list = mutableListOf<String>()
        list.addAll(
            listOf(
                "1499.99$",
                "349.99$",
                "989.99$",
                "119.99$",
                "4.99$",
                "249.99$"
            )
        )
        val list1 = list[0]
        val list2 = list[1]
        val list3 = list[2]
        val list4 = list[3]
        val list5 = list[4]
        val list6 = list[5]
        (findViewById<View>(R.id.button11) as Button).text = list1
        (findViewById<View>(R.id.button13) as Button).text = list2
        (findViewById<View>(R.id.button14) as Button).text = list3
        (findViewById<View>(R.id.button15) as Button).text = list4
        (findViewById<View>(R.id.button17) as Button).text = list5
        (findViewById<View>(R.id.button16) as Button).text = list6

        val secondActButton1 = findViewById<Button>(R.id.button11)
        secondActButton1.setOnClickListener {
            val Intent = Intent(this, MainActivity3::class.java)
            startActivity(Intent)
        }
        val secondActButton3 = findViewById<Button>(R.id.button17)
        secondActButton3.setOnClickListener {
            val Intent3 = Intent(this, PaperClips::class.java)
            startActivity(Intent3)
        }
        val secondActButton4 = findViewById<Button>(R.id.button16)
        secondActButton4.setOnClickListener {
            val Intent4 = Intent(this, DirtBike::class.java)
            startActivity(Intent4)
        }
        val secondActButton5 = findViewById<Button>(R.id.button15)
        secondActButton5.setOnClickListener {
            val Intent5 = Intent(this, ChristmasTree::class.java)
            startActivity(Intent5)
        }
        val secondActButton6 = findViewById<Button>(R.id.button13)
        secondActButton6.setOnClickListener {
            val Intent6 = Intent(this, PlayStation5Pro::class.java)
            startActivity(Intent6)
        }
        val secondActButton7 = findViewById<Button>(R.id.button14)
        secondActButton7.setOnClickListener {
            val Intent7 = Intent(this, Watch::class.java)
            startActivity(Intent7)
        }
        val secondActButton2 = findViewById<Button>(R.id.imageButton)
        secondActButton2.setOnClickListener {
            val Intent1 = Intent(this, MainActivity::class.java)
            startActivity(Intent1)
        }


    }
}





