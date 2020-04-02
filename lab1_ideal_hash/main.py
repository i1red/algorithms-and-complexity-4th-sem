from idealhash import HashMap
from utils.staff import Division, Worker
from utils import serialize_objects, deserialize_objects


divisions = [
    (Division('Star Wars Jedi'), [Worker('Mace Windu'), Worker('Master Yoda'), Worker('Luke Skywalker'),
                                  Worker('Leia Organa'), ]),
    (Division('Star Wars Sith'), [Worker('Emperor Palpatine'), Worker('Darth Vader'), Worker('Count Dooku')]),
    (Division('UFC Light Heavyweight'), [Worker('Jon Jones'), Worker('Alexander Gustaffson'), Worker('Daniel Cormier')]),
    (Division('UFC Lightweight'), [Worker('Tony Ferguson'), Worker('Khabib Nurmagomedov'), Worker('Conor McGregor')]),
    (Division('Boxing Heavyweight'), [Worker('Oleksandr Usyk'), Worker('Anthony Joshua'), Worker('Deontay Wilder')]),
    (Division('Football'), [Worker('Lionel Messi'), Worker('Virgil van Dijk'), Worker('Kylian Mbappe')]),
    (Division('Avengers'), [Worker('Iron Man'), Worker('Captain America'), Worker('Ant Man')]),
    (Division('Basketball'), [Worker('LeBron James'), Worker('Stephen Curry'), Worker('Kobe Bryant')]),
    (Division('The Witcher'), [Worker('Geralt'), Worker('Coin'), Worker('Jaskier')]),
    (Division('Sherlock'), [Worker('Sherlock Holmes'), Worker('Dr Watson'), Worker('Mrs Hudson')])
]


if __name__ == '__main__':
    mapping = HashMap(list(deserialize_objects('divisions.bin')))
    print(mapping)
    print(mapping[Division('The Witcher')])

