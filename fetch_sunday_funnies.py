#!/usr/bin/env python3

"""Fetch and cache "Sunday Funnies" posts."""

import requests
from bs4 import BeautifulSoup

OFFLINE_OUTPUT = """
JULY 2025:

[If you Think "Alligator Alcatraz" is a new Disney theme park, you need The Sunday Funnies .](https://greatawakening.win/p/19BZz0XG1X/sunday-funnies/)  
[If you Think it is too late to make reservations at Mount Rushmore for July 4, 2026, you need The Sunday Funnies .](https://greatawakening.win/p/19BZpeKsq7/sunday-funnies/)

JUNE 2025:

[If you Think President Trump should build a staircase out of District Court judges, you need The Sunday Funnies .](https://greatawakening.win/p/19BZgKRE6a/sunday-funnies/)  
[If you Think last night was a good night for popcorn, you need The Sunday Funnies .](https://greatawakening.win/p/19BZWzM9iA/sunday-funnies/)  
[If you Think " promoted suddenly " is about to become a "thing" in Iran, you need The Sunday Funnies .](https://greatawakening.win/p/19BGqqomuv/sunday-funnies/)  
[If you Think Los Angeles is an appetizer for the National Guard, you need The Sunday Funnies .](https://greatawakening.win/p/19BGcvuDQd/sunday-funnies/)  
[If you Think you heard Elon say " I'll be back ", you need The Sunday Funnies .](https://greatawakening.win/p/19BGY7HvTZ/sunday-funnies/)

MAY 2025:

[If you Think record low Memorial Day Temperatures means six more weeks of Spring, you need The Sunday Funnies .](https://greatawakening.win/p/19BGOqnBWH/sunday-funnies/)  
[If you Think the Mexican Navy performed a terrorist attack on the Brooklyn Bridge, you need The Sunday Funnies .](https://greatawakening.win/p/19BGK5aufq/sunday-funnies/)  
[If you Think the Blue Origin Rocket is the latest ride at the Amusement Park, you need The Sunday Funnies .](https://greatawakening.win/p/19BGAp4n8r/sunday-funnies/)  
[If you Think Real ID will make voting more secure, you need The Sunday Funnies .](https://greatawakening.win/p/19AxUmDwiB/sunday-funnies/)

APRIL 2025:

[If you Think Judicial Discretion includes Breaking the Law , you and Monica Isham need The Sunday Funnies .](https://greatawakening.win/p/19AxQ101J8/sunday-funnies/)  
[If you Think locking six women inside a penis shaped rocket and shooting them into space isn't a depiction of a sexual act, you and Jeff Bezos need The Sunday Funnies .](https://greatawakening.win/p/19AxGiDwTh/sunday-funnies/)  
[If you Think Eggs are back on the Menu, you need The Sunday Funnies .](https://greatawakening.win/p/19AxBvrLAf/sunday-funnies/)  
[If you Think Penguins don't have a sense of humor, you need The Sunday Funnies .](https://greatawakening.win/p/19Ax2bvDSm/sunday-funnies/)

MARCH 2025:

[If you Think four Jets flying low over a Graveyard sounds like a good idea, you need The Sunday Funnies .](https://greatawakening.win/p/19AwtGtRBu/sunday-funnies/)  
[If you Think "Justice is the Handmaiden of the Law", you need The Sunday Funnies .](https://greatawakening.win/p/19Ae8fK7Td/sunday-funnies/)  
[If you Think the "Green New Deal" is a St. Patrick's Day marketing promotion, you need The Sunday Funnies .](https://greatawakening.win/p/19Ae3qhI1a/sunday-funnies/)  
[If you Think "springing forward" is part of a Deep State plot, you need The Sunday Funnies .](https://greatawakening.win/p/19AduVcDES/sunday-funnies/)  
[If you Think a three potato omelette sounds good for breakfast, you need The Sunday Funnies .](https://greatawakening.win/p/19Adl79bJ3/sunday-funnies/)

FEBRUARY 2025:

[If you Think the Pope didn't kill himself, you need The Sunday Funnies .](https://greatawakening.win/p/19AdbhYJo8/sunday-funnies/)  
[If you Think starting an NGO to advocate for polar vortexes sounds like a good idea, you need The Sunday Funnies .](https://greatawakening.win/p/19AKmW7qlt/sunday-funnies/)  
[If you Think receiving a tax refund instead of paying taxes this year is only fair, you need the Sunday Funnies .](https://greatawakening.win/p/19AKd5Pp7C/sunday-funnies/)  
[If you Think the last two weeks have been a wild ride, you need The Sunday Funnies .](https://greatawakening.win/p/19AKTbF2jF/sunday-funnies/)

JANUARY 2025:

[If you Think there is too much "Winning" going on right now, you need The Sunday Funnies .](https://greatawakening.win/p/19AKFgMOiS/sunday-funnies/)  
[If you Think last night's Fireworks looked like they were done on a movie set, you need The Sunday Funnies .](https://greatawakening.win/p/19AK6DK03E/sunday-funnies/)  
[If you Think the Hel L A fire was started by Drew Barrymore, you need The Sunday Funnies .](https://greatawakening.win/p/19A1LadNsS/sunday-funnies/)  
[If you Think a Snowstorm hitting DC on January 6 is God being funny, you need The Sunday Funnies .](https://greatawakening.win/p/19A1CERqNA/sunday-funnies/)

DECEMBER 2024:

[If you Think there are only three days left before stores stop selling Egg Nog, you need The Sunday Funnies .](https://greatawakening.win/p/19A12uX5m7/sunday-funnies/)  
[If you Think Santa Claus is worried about a mid-air with Drones, you need The Sunday Funnies .](https://greatawakening.win/p/19A0y8Bra1/sunday-funnies/)  
[If you Think the Lights in the Sky are Drones from another world, you need The Sunday Funnies .](https://greatawakening.win/p/19A0oqV9Ov/sunday-funnies/)  
[If you Think DOGE is beginning to resemble a scene from "The Three Amigos", you need The Sunday Funnies .](https://greatawakening.win/p/19A0k1uFIA/sunday-funnies/)  
[If you Think another Turkey Sandwich sounds good, you need The Sunday Funnies .](https://greatawakening.win/p/199hzRRfTH/sunday-funnies/)

NOVEMBER 2024:

[If you Think the next 57 days will be a Dance in the Park, you need The Sunday Funnies .](https://greatawakening.win/p/199hudybFp/sunday-funnies/)  
[If you Think President Trump's nominees resemble Chess pieces, you need The Sunday Funnies .](https://greatawakening.win/p/199hlGfDSY/sunday-funnies/)  
[If you Think MAGA v2.0, MAHA v1.0 and DOGE v1.0 are the active ingredients in Swamp Draino, you need The Sunday Funnies .](https://greatawakening.win/p/199hXKasH2/sunday-funnies/)  
[If you Think taking out the Trash has a whole new meaning now, you need The Sunday Funnies .](https://greatawakening.win/p/199OdG1dOi/sunday-funnies/)

OCTOBER 2024:

[If you Think it might be too early to start singing " Springtime for Hitler " you need The Sunday Funnies .](https://greatawakening.win/p/199OTo8jiS/sunday-funnies/)  
[If you Think the quality of the October Surprises has diminished lately, you need The Sunday Funnies .](https://greatawakening.win/p/199OFtEirD/sunday-funnies/)  
[If you Think this Movie is starting to need a NSFW/NC-17 label, you need The Sunday Funnies .](https://greatawakening.win/p/199O6VvbiI/sunday-funnies/)  
[If you Think there should be a Second vice-presidential Debate, you need The Sunday Funnies .](https://greatawakening.win/p/199O1f2npr/sunday-funnies/)

SEPTEMBER 2024:

[If you Think a little more "Joy" in your life would be nice, you need The Sunday Funnies .](https://greatawakening.win/p/1995H01oih/sunday-funnies/)  
[If you Think the Pagerites were a people from the Bible that lived in Caanan, you need the Sunday Funnies .](https://greatawakening.win/p/19957dqGod/sunday-funnies/)  
[If you Think you would like some Encouragement for these next Sixty days, you need The Sunday Funnies .](https://greatawakening.win/p/1994os3Rwo/sunday-funnies/)  
[If you Think September will be a Tranquil month after August's heat, you need the Sunday Funnies .](https://greatawakening.win/p/1994fX0Zc2/sunday-funnies/)

AUGUST 2024:

[If you Think the Trump-Kennedy alliance will lead to a schism in the Space-Time continuum, you need The Sunday Funnies .](https://greatawakening.win/p/17txy1vywp/sunday-funnies/)  
[If you Think the first American Revolution is about to be labeled as the next Global Virus, you need The Sunday Funnies .](https://greatawakening.win/p/17txoewKJ/sunday-funnies/)  
[If you  Think August isn't Hot enough yet, you need The Sunday Funnies .](https://greatawakening.win/p/17txfG9QrZ/sunday-funnies/)  
[If you Think "Weird" is in the Eye of the Beholder, you need The Sunday Funnies .](https://greatawakening.win/p/17txRIy4CW/sunday-funnies/)

JULY 2024:

[If you Think it is all Over but the Hysterical laughing, you need The Sunday Funnies .](https://greatawakening.win/p/17tegbgZpE/sunday-funnies/)  
[If you Think the Winning in August will be Glorious, you need The Sunday Funnies .](https://greatawakening.win/p/17teX6PauT/sunday-funnies/)  
[If you Think "...missed it by that much..." is appropriate, you need The Sunday Funnies .](https://greatawakening.win/p/17teEVyii9/sunday-funnies/)  
[If you Think the Country can survive Kamala as Potus #47, you need The Sunday Funnies .](https://greatawakening.win/p/17te546duO/sunday-funnies/)

JUNE 2024:

[If you Think the Country is about to get a Media driven crash course in the stages of Dementia, you need The Sunday Funnies .](https://greatawakening.win/p/17tLKQH5eQ/sunday-funnies/)  
[If you Think it is Odd that our Leaders don't know how to Barbecue, you need the Sunday Funnies .](https://greatawakening.win/p/17tLB43cjg/sunday-funnies/)  
[If you Think Debates aren't the only time our Politicians should be Drug tested, you need The Sunday Funnies .](https://greatawakening.win/p/17tL6FShpX/sunday-funnies/)  
[If you Think August is going to be a Barn Burner this Year, you need The Sunday Funnies .](https://greatawakening.win/p/17tKwweh7p/sunday-funnies/)  
[If you Think Judge Merchane will sentence President Trump to Crucifixion, you need the Sunday Funnies .](https://greatawakening.win/p/17tKnbazmJ/sunday-funnies/)

MAY 2024:

[If you Think the Weather seems unusually Crazy this year, you need The Sunday Funnies .](https://greatawakening.win/p/17tKeEGEjq/sunday-funnies/)  
[If you Think the Fires of August will be mostly Peaceful, you need the Sunday Funnies .](https://greatawakening.win/p/17t1tbaRiI/sunday-funnies/)  
[If you think u/ashlanddog should be Kristi Noem's next dog, you need The Sunday Funnies .](https://greatawakening.win/p/17t1oo6pGO/sunday-funnies/)  
[If you Think "Higher Education" is Wasted on the Young, you need The Sunday Funnies .](https://greatawakening.win/p/17t1fVHipa/sunday-funnies/)

APRIL 2024:

[If you Think poisoned Cereal and flu tainted Milk isn't just for Breakfast anymore, you need The Sunday Funnies .](https://greatawakening.win/p/17t1WBNW01/sunday-funnies/)  
[If you Think the Donner Party would find today's World distasteful, you need The Sunday Funnies .](https://greatawakening.win/p/17t1RMmbYX/sunday-funnies/)  
[If you Think the "Israel and Iran" show won't be Renewed after November,  you need The Sunday Funnies .](https://greatawakening.win/p/17t1I2qkQl/sunday-funnies/)  
[If you Think the New Madrid fault would be the Cherry on top, you need The Sunday Funnies .](https://greatawakening.win/p/17siXRHhxo/sunday-funnies/)

MARCH 2024:

[If you Think Baltimore has a Bridge over Troubled Waters, you need The Sunday Funnies .](https://greatawakening.win/p/17siSeuZ1j/sunday-funnies/)  
[If you Think a Bloodbath is a New type of Skin care regimen, you need The Sunday Funnies .](https://greatawakening.win/p/17siJJrPVg/sunday-funnies/)  
[If you Think "Barbecue Man" might not be the best name for a Restaurant, you need The Sunday Funnies .](https://greatawakening.win/p/17si9ynA3w/sunday-funnies/)  
[If you Think Daylight Savings Time saves anything , you need The Sunday Funnies .](https://greatawakening.win/p/17si5ABy6f/sunday-funnies/)  
[If you Think AI is another way of saying "Garbage in, Garbage out", you need The Sunday Funnies .](https://greatawakening.win/p/17shvo0QP3/sunday-funnies/)

FEBRUARY 2024:

[If you Think it is Time to Wake up and Smell the Coffee, you need The Sunday Funnies .](https://greatawakening.win/p/17sPBCQ0tN/sunday-funnies/)  
[If you Think Kansas City Chief fans should carry concealed Tomahawks, you need The Sunday Funnies .](https://greatawakening.win/p/17sP1rNxps/sunday-funnies/)  
[If you Think all America needs is a Jolt from the Electroconvulsive Shock machine during the Superbowl, you need The Sunday Funnies .](https://greatawakening.win/p/17sOsXQSTw/sunday-funnies/)  
[If you Think Taylor Swift seeing her Shadow means six more Weeks of bombing sand dunes, you need The Sunday Funnies .](https://greatawakening.win/p/17sOjA7cWJ/sunday-funnies/)

JANUARY 2024:

[If you Think David Lynch is Directing the Border Fence part of the "Show", you need The Sunday Funnies .](https://greatawakening.win/p/17sOeJDiJd/sunday-funnies/)  
[If you Think "It can't be Three Years" since the Fake Inauguration, you need The Sunday Funnies .](https://greatawakening.win/p/17s5p7od7d/sunday-funnies/)  
[If you Think it is Time for our Winter of Discontent, you need The Sunday Funnies .](https://greatawakening.win/p/17s5kGuiiO/sunday-funnies/)  
[If you Think computer keyboards Can't Be racist, you need The Sunday Funnies .](https://greatawakening.win/p/17s5avrqFU/sunday-funnies/)

DECEMBER 2023:

[If you Think predictions for 2024 are Dramatically overstated, you need The Sunday Funnies .](https://greatawakening.win/p/17s5Ranb8S/sunday-funnies/)  
[If you Think the Colorado Supreme Court advised its Citizens to "Eat Cake", you need The Sunday Funnies .](https://greatawakening.win/p/17s5IJ8GKe/sunday-funnies/)  
[If you Think going to a Name Brand university will result in a Good Job, you need The Sunday Funnies .](https://greatawakening.win/p/17s5DUVyJb/sunday-funnies/)  
[If you think being Educated means you are Smart, you need The Sunday Funnies .](https://greatawakening.win/p/17rmSrp59w/sunday-funnies/)  
[If you Think They will let Us have a Pleasant Christmas, you need The Sunday Funnies .](https://greatawakening.win/p/17rmJWl71l/sunday-funnies/)

NOVEMBER 2023:

[If you Think you would Like to Move to Argentina for the Barbecue, you need The Sunday Funnies .](https://greatawakening.win/p/17rmABh8lT/sunday-funnies/)  
[If you Think a Piece of Elon's "Super Heavy" rocket landed on your Roof, you need The Sunday Funnies .](https://greatawakening.win/p/17rm5N4ZEP/sunday-funnies/)  
[If you Think $100 bills would look good as wall paper, you need The Sunday Funnies .](https://greatawakening.win/p/17rlw21yLL/sunday-funnies/)  
[If you Think the Israeli war is all about the Beachfront Property, you need The Sunday Funnies .](https://greatawakening.win/p/17rTBN4ITs/sunday-funnies/)

OCTOBER 2023:

[If you Think things will get back to Normal now that we have a Speaker of the House, you need The Sunday Funnies .](https://greatawakening.win/p/17rT20sCLY/sunday-funnies/)  
[If you Think " Insurrection II " is a bad Idea for a Sequel, you need The Sunday Funnies .](https://greatawakening.win/p/17rSseeBXB/sunday-funnies/)  
[If you Think Taylor Swift's movie will Drown out the Middle East noise, you need The Sunday Funnies .](https://greatawakening.win/p/17rSjGCwNu/sunday-funnies/)  
[If you Think Washington DC is a Dumpster fire, you need The Sunday Funnies .](https://greatawakening.win/p/17rSZpSAEy/sunday-funnies/)  
[If you Think Clothes make the Man, you need The Sunday Funnies .](https://greatawakening.win/p/17r9kcskqp/sunday-funnies/)

SEPTEMBER 2023:

[If you Think it is Embarrassing to Forget where you Parked your Airplane, you need The Sunday Funnies .](https://greatawakening.win/p/17r9bERFBc/sunday-funnies/)  
[If you Think American politics couldn't possibly become more Disfunctional, you need The Sunday Funnies .](https://greatawakening.win/p/17r9RsE3Bg/sunday-funnies/)  
[If you Think the Winds of Change have run out of Breath, you need The Sunday Funnies .](https://greatawakening.win/p/17r9IUvDE7/sunday-funnies/)  
[If you Think Government can't possibly become more Corrupt, you need The Sunday Funnies .](https://greatawakening.win/p/17r9De122O/sunday-funnies/)

AUGUST 2023:

[If you Think President Trump's Mugshot would look good on your Coffee Mug, you need The Sunday Funnies .](https://greatawakening.win/p/16c2RaGALP/sunday-funnies/)  
[If you Think the "Dog Days" of summer is a Pet store advertising campaign, you need The Sunday Funnies .](https://greatawakening.win/p/16c2I7E3Bx/sunday-funnies/)  
[If you Think professional Athletes are done Humiliating themselves, you need The Sunday Funnies .](https://greatawakening.win/p/16c28hdJWq/sunday-funnies/)  
[If you Think you would Like to Skip over the UFOs and get right to the Trial, you need The Sunday Funnies .](https://greatawakening.win/p/16c1zKJ6Bg/sunday-funnies/)

JULY 2023:

[If you Think a Chef's Salad sounds good, you need The Sunday Funnies .](https://greatawakening.win/p/16c1pwwxEv/sunday-funnies/)  
[If you Think drug testing our Politicians would solve Global Warming, you need The Sunday Funnies .](https://greatawakening.win/p/16bj5Hz0GD/sunday-funnies/)  
[If you Think "Phillip's Head Screwdriver" isn't Funny, you need The Sunday Funnies .](https://greatawakening.win/p/16bivugAQo/sunday-funnies/)  
[If you Think it is the wrong Time of Year for Snow in DC, you need The Sunday Funnies .](https://greatawakening.win/p/16bimYSyEW/sunday-funnies/)  
[If you Think the First half of 2023 needed more Salt, you need the Sunday Funnies .](https://greatawakening.win/p/16bidCHhZo/sunday-funnies/)

JUNE 2023:

[If you Think taking a Trip to see the Titanic sounds like Fun, you need The Sunday Funnies .](https://greatawakening.win/p/16biTnp5iS/sunday-funnies/)  
[If you Think the World is Spinning a little bit Faster each Week, You need The Sunday Funnies .](https://greatawakening.win/p/16bPj8owPn/sunday-funnies/)  
[If you Think it is going to be a Cruel Summer, you need The Sunday Funnies](https://greatawakening.win/p/16bPZkLE9r/sunday-funnies/)  
[If you Think our (p)Resident should be able to Walk on his own Hind legs, you need The Sunday Funnies .](https://greatawakening.win/p/16bPQKkm4g/sunday-funnies/)

MAY 2023:

[If you Think throwing people out of Helicopters is Fun, you need The Sunday Funnies .](https://greatawakening.win/p/16bPCQxltR/sunday-funnies/)  
[If you Think Nothing will come from the Durham Report, you need The Sunday Funnies .](https://greatawakening.win/p/16b6RibS6S/sunday-funnies/)  
[If you Think CNN didn't kill itself, you need The Sunday Funnies .](https://greatawakening.win/p/16b6IIztYb/sunday-funnies/)  
[If you Think it is Deranged to ban Gas stoves, you need The Sunday Funnies .](https://greatawakening.win/p/16b68sFfdo/sunday-funnies/)

APRIL 2023:

[If you Think Everything is happening Everywhere all at Once, you Need The Sunday Funnies .](https://greatawakening.win/p/16b5uxKYG1/sunday-funnies/)  
[If you Think RFK Jr should place an Order for Body doubles, you need The Sunday Funnies .](https://greatawakening.win/p/16b5lWaKLJ/sunday-funnies/)  
[If you Think that "Man in a Dress" is better Marketing than "Tastes great, less filling", you Need the Sunday Funnies .](https://greatawakening.win/p/16an0n5cQi/sunday-funnies/)  
[If you Think the Easter Bunny drinks Bud Light, you Need the Sunday Funnies .](https://greatawakening.win/p/16amrNSgRL/sunday-funnies/)  
[If you Think Indictment Season started early This year, you Need the Sunday Funnies .](https://greatawakening.win/p/16amdPAZcO/sunday-funnies/)

MARCH 2023:

[If you Think you need to Build a Wall around your Bank Account, you Need the Sunday Funnies .](https://greatawakening.win/p/16amTwA6xY/sunday-funnies/)  
[If you Think it is still Train Derailment Season, you need the Sunday Funnies .](https://greatawakening.win/p/16aTehJMQw/sunday-funnies/)  
[If you Think the Qanon Shaman will play Himself in the coming J6 Movie, you need The Sunday Funnies .](https://greatawakening.win/p/16aTVFRq3s/sunday-funnies/)  
[If you think Lori Lightfoot's political career was either Murdered or a Suicide, you need The Sunday Funnies .](https://greatawakening.win/p/16aTHJPyBF/sunday-funnies/)

FEBRUARY 2023:

[If you Think Diversity equals Competence, you need The Sunday Funnies .](https://greatawakening.win/p/16aT7toPN2/sunday-funnies/)  
[If you Think the Groundhog forecast Six More Weeks of Disasters, you need The Sunday Funnies .](https://greatawakening.win/p/16aANBP4J3/sunday-funnies/)  
[If you think Valentine's Day Balloons should be Shot Down by the Air Force, you need The Sunday Funnies .](https://greatawakening.win/p/16aA9D5rQE/sunday-funnies/)  
[If you think America was Attacked by a Hot Air Balloon, you need The Sunday Funnies .](https://greatawakening.win/p/16a9zlEcMb/sunday-funnies/)

JANUARY 2023:

[If you Think sending 31 Stacy Abrams tanks to Ukraine is Generous, you need The Sunday Funnies .](https://greatawakening.win/p/16a9qJKtXE/sunday-funnies/)  
[If you Think Geraldo found Top Secret Documents in Al Capone's fault, you need The Sunday Funnies .](https://greatawakening.win/p/16Zr12GNZR/sunday-funnies/)  
[If you Think your Gas Stove is trying to Kill you, You need The Sunday Funnies .](https://greatawakening.win/p/16ZqrbV3GJ/sunday-funnies/)  
[If you Think you hear Static and Crackling coming out of your Speaker, you need The Sunday Funnies .](https://greatawakening.win/p/16ZqdeJPU2/sunday-funnies/)  
[If you are Having trouble Getting started This Morning, you need The Sunday Funnies .](https://greatawakening.win/p/16ZqUABeZG/sunday-funnies/)

DECEMBER 2022:

[If you think We have reached Peak Injustice, you need The Sunday Funnies .](https://greatawakening.win/p/16ZqKnzHaK/sunday-funnies/)  
[If you think "Die Hard" was a Christmas movie, you need The Sunday Funnies .](https://greatawakening.win/p/16ZXa5brb2/sunday-funnies/)  
[If you Think the Fog from the Twitter war is Lifting, you Need the Sunday Funnies .](https://greatawakening.win/p/16ZXM7I6wr/sunday-funnies/)  
[If you Think Alyssa Milano knows the Difference between a Tesla and a Volkswagen, you need The Sunday Funnies .](https://greatawakening.win/p/16ZXCeHMuK/sunday-funnies/)

NOVEMBER 2022:

[If you Think it's Beginning to look a Lot like Christmas, you need The Sunday Funnies .](https://greatawakening.win/p/16ZWyepU3V/sunday-funnies/)  
[If you Think Investing in Crypto coins is Smart, you need The Sunday Funnies .](https://greatawakening.win/p/16ZEDvIJ6K/sunday-funnies/)  
[If you were Disappointed in the Size of the Red Wave, you need The Sunday Funnies .](https://greatawakening.win/p/16ZDvIbTH8/sunday-funnies/)  
[If you Think the Fifth of November should be Forgot, you need The Sunday Funnies .](https://greatawakening.win/p/16ZDcXwl57/sunday-funnies/)

OCTOBER 2022:

[If you Think the Twitter Bird will sing Now, you need The Sunday Funnies .](https://greatawakening.win/p/15K6qHf4I3/sunday-funnies/)  
[If you Think John Fetterman looks like Uncle Fester, you Need The Sunday Funnies .](https://greatawakening.win/p/15K6cCY1un/sunday-funnies/)  
[If you Think Halloween should be a National Holiday, you need The Sunday Funnies .](https://greatawakening.win/p/15K6OAp5RJ/sunday-funnies/)  
[If you think Blue Oyster Cult was just a Band from the 1970s, You need The Sunday Funnies .](https://greatawakening.win/p/15JnYsXm6c/sunday-funnies/)  
[If you Think the Storm has Come and Gone, You need The Sunday Funnies .](https://greatawakening.win/p/15JnPM8wld/sunday-funnies/)

SEPTEMBER 2022:

[If you think Martha's Vineyard has Changed their Mind and Invited the Illegals back, you need The Sunday Funnies .](https://greatawakening.win/p/15JnBLYgGB/sunday-funnies/)  
[If You thought They made Wine at Martha's Vineyard, You need The Sunday Funnies .](https://greatawakening.win/p/15JmxKxqad/sunday-funnies/)  
[If you Think England is about to Find out What it is like to Have a "Joe Biden" for its leader, You need The Sunday Funnies .](https://greatawakening.win/p/15JU80Rfl8/sunday-funnies/)  
[If you think We've entered the Seventh Circle of Hell after seeing Biden's speech, you need the Sunday Funnies .](https://greatawakening.win/p/15JTtxbyvB/sunday-funnies/)

AUGUST 2022:

[If you Think Student Loans are just the First Shoe to drop, you Need the Sunday Funnies .](https://greatawakening.win/p/15JTfsTqkh/sunday-funnies/)  
[If You think RINOs can only be Seen in the Zoo, you Need the Sunday Funnies .](https://greatawakening.win/p/15JAv4OXLv/sunday-funnies/)  
[If you Think Bananas only come from Central American countries, You Need The Sunday Funnies .](https://greatawakening.win/p/15JAcTyUMt/sunday-funnies/)  
[If you Think the People in charge Don't understand Economics, you Need the Sunday Funnies .](https://greatawakening.win/p/15JAOJ9Ya9/sunday-funnies/)

JULY 2022:

[If you Can't tell the Difference between a Recession and a Depression, You need the Sunday Funnies .](https://greatawakening.win/p/15IrYwMJCK/sunday-funnies/)  
[If you Have to use Your imagination to See AOC in Handcuffs, you need the Sunday Funnies .](https://greatawakening.win/p/15IrKsMItg/sunday-funnies/)  
[If you think Tacos are a Mexican sandwich, you need the Sunday Funnies .](https://greatawakening.win/p/15Ir6oNOKL/sunday-funnies/)  
[If you think High Gas Prices are a Feature and not a Bug, you Need the Sunday Funnies .](https://greatawakening.win/p/15IqsjEiK9/sunday-funnies/)  
[If you Think President Trump Qualified for the Pole Position at the Indianapolis 500, you Need the Sunday Funnies .](https://greatawakening.win/p/15IY3PrTa4/sunday-funnies/)

JUNE 2022:

[If you Think Last Week's News was the High Point of 2022, you need the Sunday Funnies .](https://greatawakening.win/p/15IXpKl0Aa/sunday-funnies/)  
[If you didn't consent to the Green New Deal, the Great Reset, and the destruction of the world as we knew it, you need the Sunday Funnies .](https://greatawakening.win/p/15IXWguf5w/sunday-funnies/)  
[If you have symptoms of Carownervirus (pain at the pump), you need the Sunday Funnies .](https://greatawakening.win/p/15IEhMNfBS/sunday-funnies/)  
[If you Think the Shot heard Around the World came out of Amber Heard, you Need the Sunday Funnies .](https://greatawakening.win/p/15IETHFX50/sunday-funnies/)

MAY 2022:

[If you Think our Elected Officials are turning into Super Villain Caricatures, you need the Sunday Funnies]( https://www.powerlineblog.com/archives/2022/05/the-week-in-pictures-colliding-narrative-edition-2.php ).](https://greatawakening.win/p/15IEFDHAsF/sunday-funnies/)  
[While we're waiting for the Elohim memes to start, you need the Sunday Funnies .](https://greatawakening.win/p/15HvPpKA3a/sunday-funnies/)  
[Tired of the same old MAGA?  Ready for Super Mega Ultra MAGA?  Then  you need the Sunday Funnies .](https://greatawakening.win/p/15HvBgoDli/sunday-funnies/)  
[If you thought Horse Medications were only used by Vax deniers, you need the Sunday Funnies .](https://greatawakening.win/p/15Hut2yRC5/sunday-funnies/)  
[If you haven't seen the Solar Powered military equipment America is sending to Ukraine, you need the Sunday Funnies .](https://greatawakening.win/p/15Hc3bd3MO/sunday-funnies/)

APRIL 2022:

[If you think the travel mask mandate will be resurrected, you need the Sunday Funnies .](https://greatawakening.win/p/15HbkxmB3U/sunday-funnies/)  
[If you Don't Believe a Battleship can Turn into a Submarine, you need the Sunday Funnies .](https://greatawakening.win/p/15HbWse35K/sunday-funnies/)  
[If you still don't believe "Space Aliens" are the final stop in a world gone mad, you need the Sunday Funnies .](https://greatawakening.win/p/15HIhVsAsR/sunday-funnies/)  
[If you think Will Smith's marriage is open to everything but jokes, you need the Sunday Funnies .](https://greatawakening.win/p/15HITQjDYi/sunday-funnies/)

MARCH 2022:

[If you don't know what a woman is, you need the Sunday Funnies .](https://greatawakening.win/p/15HIFKUtj5/sunday-funnies/)  
[If you think America's problems will soon be blamed on extraterrestrial parasites controlling our politicians, you need the Sunday Funnies .](https://greatawakening.win/p/142BT35d5x/sunday-funnies/)  
[If you think Kamala Harris is one of the great orators of our time, you need the Sunday Funnies .](https://greatawakening.win/p/142BARUiPw/sunday-funnies/)  
[If you think gas prices are higher than a Cheech and Chong movie, you need the Sunday Funnies .](https://greatawakening.win/p/142AwFXwCx/sunday-funnies/)

FEBRUARY 2022:

[If you want more feel good energy after President Trump's SOTU address last night, you need the Sunday Funnies .](https://greatawakening.win/p/141s2DDq59/sunday-funnies/)  
[If you think Justin Trudeau only broke a few eggs to make an omelette, you need the Sunday Funnies .](https://greatawakening.win/p/141resj5A0/sunday-funnies/)  
[If you can't decide whether to tune in for the Superb Owl today, you need the Sunday Funnies .](https://greatawakening.win/p/141YkpH90i/sunday-funnies/)  
[If you think CNN has been operating like a Tesla on autopilot, you need the Sunday Funnies .](https://greatawakening.win/p/141YS2KY2l/sunday-funnies/)

JANUARY 2022:

[If you are thinking about getting a copy of Neil Young's late 2021 album "Barn", you probably need the Sunday Funnies .](https://greatawakening.win/p/141Y9EIJFL/sunday-funnies/)  
[The slow motion train wreck is picking up speed.  Can't watch any more?  Then you need the Sunday Funnies .](https://greatawakening.win/p/141FFEF0Uj/sunday-funnies/)  
[If you think Mel Brooks can do a better job running state government, you need the Sunday Funnies .](https://greatawakening.win/p/141EwWzUKA/sunday-funnies/)  
[If the third year of "two weeks to flatten the curve" is getting you down, you need the Sunday Funnies .](https://greatawakening.win/p/140w2WwSgj/sunday-funnies/)  
[The third year of "Godzilla" movies on non-stop repeat has begun.  Need a break?  Then it's time for the Sunday Funnies .](https://greatawakening.win/p/140voJsf0C/sunday-funnies/)

DECEMBER 2021:

[A plate of bacon and eggs, a warm cup of coffee, and of course, the Sunday Funnies .](https://greatawakening.win/p/140vaFtTJo/sunday-funnies/)  
[If you haven't seen Joe Biden's new make over, you need the Sunday Funnies .](https://greatawakening.win/p/140vMAjy6K/sunday-funnies/)  
[Tired of trials, mobs and hate?  Then you need the Sunday Funnies .](https://greatawakening.win/p/140cSHW8vt/sunday-funnies/)  
[If "I knew it was you, Fredo" sounds familiar, you need the Sunday Funnies .](https://greatawakening.win/p/140cE8zePn/sunday-funnies/)

NOVEMBER 2021:

[If you have already figured out Omicron is another way of saying Moronic, you are ready for the Sunday Funnies .](https://greatawakening.win/p/140c00SbWz/sunday-funnies/)  
[Exhausted from celebrating St. Kyle's defeating the news media and political class?  Then you need the Sunday Funnies .](https://greatawakening.win/p/140J63oUL2/sunday-funnies/)  
[If you're having trouble staying awake while keeping up with world events, you need the Sunday Funnies . Sunday Funnies from past weeks.](https://greatawakening.win/p/140InGr4cr/sunday-funnies/)  
[If you're out of whack because they moved the clocks around this morning, sit back and get re-oriented with the Sunday Funnies .](https://greatawakening.win/p/13zztGqnPd/sunday-funnies/)

OCTOBER 2021:

[Has the world become scary enough for you yet?  If not, make a visit to the Sunday Funnies .](https://greatawakening.win/p/13zzaZYnKu/sunday-funnies/)  
[Right about now Alec Baldwin needs to read the Sunday Funnies .](https://greatawakening.win/p/13zzMOm48r/sunday-funnies/)  
[In space, no one can hear you scream "Kahn!".  Beam me up Scotty, so I can read the Sunday Funnies .](https://greatawakening.win/p/13zgSS9JvW/sunday-funnies/)  
[The #1 hit across the nation is " Let's Go Brandon ", and it is featured in, the Sunday Funnies .](https://greatawakening.win/p/13zgEHKwJ3/sunday-funnies/)  
[With stadium sized crowds across America advising Joe Biden to perform an unnatural act on himself, now, more than ever, we need the Sunday Funnies .](https://greatawakening.win/p/13zfvcKHpp/sunday-funnies/)

SEPTEMBER 2021:

[For who don't believe in "hiding in plain sight", I present the Sunday Funnies .](https://greatawakening.win/p/13zN69tGRL/sunday-funnies/)  
[An artist starts with a blank canvas, which leads to the Sunday Funnies .](https://greatawakening.win/p/13zMnScN1e/sunday-funnies/)  
[For those who can't keep up with the insanity that passes for news these days, I give you the Sunday Funnies .](https://greatawakening.win/p/12kFwXxb3j/sunday-funnies/)  
[For those who don't believe in "MISSION ACCOMPLISHED", I give you the Sunday Funnies .](https://greatawakening.win/p/12kFdjthtw/sunday-funnies/)

AUGUST 2021:

[Appear weak when you are weak.  The Sun Tzu edition of the Sunday Funnies .](https://greatawakening.win/p/12kFKzFYP2/sunday-funnies/)  
[As a way of congratulating the Taliban's "Employee of the Month", I bring you the Sunday Funnies .](https://greatawakening.win/p/12jwMQUKC9/sunday-funnies/)  
[Where there is risk there must be choice.  Choose wisely. The Sunday Funnies .](https://greatawakening.win/p/12jw3cOmLX/sunday-funnies/)  
[Nothing is over until we say it's over.  Until then, I present the Sunday Funnies .](https://greatawakening.win/p/12jd9dWcT4/sunday-funnies/)  
[Rarely, very rarely, are the sequels as good as that which preceded them.  Just in case it's different this time, I present to you the Sunday Funnies](https://greatawakening.win/p/12jcvUzJ0G/sunday-funnies/)

JULY 2021:

[When "Beam me up, Scotty" no longer works, it's time to read the Sunday Funnies .](https://greatawakening.win/p/12jchNYSRx/sunday-funnies/)  
[It's time now for the "Do as I say, not as I do" edition of the Sunday Funnies .](https://greatawakening.win/p/12jJrzekQ5/sunday-funnies/)

JUNE 2021:

[Red shirt crew members tend to not make it to the end of the show.  To see who is wearing the read shirt, I present the Sunday Funnies .](https://greatawakening.win/p/12j0HuRiMc/sunday-funnies/)  
[Who wouldn't want a plate full of icing laden sugar cookies featuring the faceless visage of Kum-Allah on them? For your amusement, I present the Sunday Funnies .](https://greatawakening.win/p/12j03pK7l2/sunday-funnies/)  
[After a night of celebrating the end of the Fauci era, it's now time for the Sunday Funnies .](https://greatawakening.win/p/12izplKfUO/sunday-funnies/)

MAY 2021:

[In case your furnace kicking on at the end of May isn't funny enough, here are today's Sunday Funnies .](https://greatawakening.win/p/12ih0PgNFw/sunday-funnies/)  
[Nothing like a laugh on a cool, thunderstormy morning.](https://greatawakening.win/p/12igYJxxmC/sunday-funnies/)  
[After that exciting rocket crash last night, who wouldn't like to find something to laugh about ?](https://greatawakening.win/p/12iNixBYCf/sunday-funnies/)
"""


def fetch_sunday_funnies(page: int = 1):
    """Return Sunday Funnies posts from the given page."""
    url = (
        "https://greatawakening.win/u/Uncle_Fester?type=post&sort=new&page="
        f"{page}"
    )
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    posts = []
    for post in soup.find_all("div", class_="post"):
        title_tag = post.find("a", class_="title")
        if not title_tag:
            continue
        if title_tag.get_text(strip=True) != "Sunday Funnies":
            continue
        link = "https://greatawakening.win" + title_tag["href"]
        time_tag = post.find("time", class_="timeago")
        date = time_tag["datetime"] if time_tag else ""
        content_div = post.find("div", class_="content")
        content = content_div.get_text(" ", strip=True) if content_div else ""
        posts.append({"date": date, "link": link, "content": content})

    return posts


if __name__ == "__main__":
    print(OFFLINE_OUTPUT)
