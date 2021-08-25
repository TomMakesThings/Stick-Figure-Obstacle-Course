<div align="center">
  <h1>Stick Figure Genetic Algorithm Obstacle Course Solver</h1>
  <p><b>NEA computer science project by <a href="https://github.com/TomMakesThings">TomMakesThings</a> - 2017/2018</b></p>
  <br>
</div>

<h1 align="center">🅐🅑🅞🅤🅣</h1>
  
<h3>Summary</h3>
<p>This application runs a custom genetic algorithm that optimises generations of stick figures so that over time they improve at navigating obstacles including spikes, pits, and caves. The code was written in Python 3.5 and GUI displayed using Tkinter.</p>

<h3>Terminology</h3>

<table>
    <thead>
        <tr>
            <th>Term</th>
            <th>Explanation</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left" valign="top">Genetic algorithms</td>
            <td align="left" valign="top">Heuristic search algorithms that use techniques inspired by natural selection, including selection, mutation and inheritance</td>
        </tr>
        <tr>
            <td align="left" valign="top">Generation</td>
            <td align="left" valign="top">The population of stick figures in each iteration</td>
        </tr>
        <tr>
            <td align="left" valign="top">Genotype</td>
            <td align="left" valign="top">The set of properties, in this case actions, that can be mutated and altered</td>
        </tr>
        <tr>
            <td align="left" valign="top">Crossover</td>
            <td align="left" valign="top">Combining genomes from two stick figures</td>
        </tr>
        <tr>
            <td align="left" valign="top">Mutation</td>
            <td align="left" valign="top">A random change the genotype, such as swapping one attribute for another, addition or deletion</td>
        </tr>
    </tbody>
</table>

<h1 align="center">🅓🅔🅢🅘🅖🅝</h1>
<p>At the start, the initial population of non-playable stick figures are created with the aim that over time their descendants will learn to navigate their way around obstacles placed within the environment. Each is assigned a unique genotype consisting of randomly generated actions including: walk, jump, stand. These are encoded as 'W', 'J' or 'S' retrospectively. The most successful individuals of this population then pass their genotypes to offspring through crossover and mutation.</p>

<p align="center"><img src="https://github.com/TomMakesThings/Stick-Figure-Obstacle-Course/blob/assets/Images/Start.png" width="100%"></p>

<p>At the beginning of each generation, all stick figures start with 100 health. If they collides with an obstacle, they will loose health as follows:</p>

<ul>
  <li>Walking into a pit causes 100 damage causing that individual's turn to end</li>
  <li>Walking into a spike causes 25 damage</li>
  <li>Jumping while walking through a cave causes 5 damage</li>
</ul>

<p align="center"><sub><b>Flowchart of stick figure life cycle</b></sub></p>
<p align="center"><img src="https://github.com/TomMakesThings/Stick-Figure-Obstacle-Course/blob/assets/Images/Lifecycle-Flowchart.png" width=600></p>
  
<h1 align="center">🅘🅝🅢🅣🅡🅤🅒🅣🅘🅞🅝🅢</h1>
  
➊ Download the code from the repository
  
➋ Extract the contents of the zip
  
➌ Open a terminal with Python installed
  
➍ Navigate to the folder of the code
  
➎ Run `python Simulator.py`

<p><img src="https://github.com/TomMakesThings/Stick-Figure-Obstacle-Course/blob/main/People/Person0W.gif" width="200"></p>
