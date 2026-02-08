# [Expert](https://www.youtube.com/watch?v=BKorP55Aqvg)

## Phases

1. Init Phase
2. Open Phase
3. Transfer Phase
4. Closing Phase


::: notes
1. Commandline is parsed and logging is initialized
2. Open Phase
  - Open First Address  (Usually Blocking)
  - Open Second Address (Usually Blocking)
3. Transfer Phase
  - watch both streams read & write
  - select
  - if required newline character conversion
4. When one of the streams reaches EOF, the closing phase begins 
:::

## Bi-Directional
(Default)

![](bi-directional-white.png)


## Unidirectional

![](unidirectional-white.png)

## Bi-Directional + Split
(Dualaddress)

![](bi-directional-split.png)


