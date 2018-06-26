var words = ['cat', 'bird', 'fish', 'hamster', 
    'lion', 'tiger', 'elephant', 'giraffe', 'hippo', 'buffalo',
    'camel', 'anteater', 'rhino', 'boar', 'tapir', 'lemur',
    'cheetah', 'zebra', 'wombat', 'leopard', 'meerkat',
    'porcupine', 'puma', 'antelope', 'gazelle',
    'bear', 'deer', 'elk', 'bison', 'fox', 'woodpecker',
    'beaver', 'otter', 'seal', 'chipmunk', 'racoon', 
    'squirrel', 'opossum', 'hare', 'platypus',
    'eagle', 'hawk', 'starling', 'cardinal', 'oriole', 'robin',
    'owl', 'sparrow', 'pigeon', 'dove', 'finch', 'magpie',
    'ostrich', 'emu', 'heron', 'bluebird', 'blackbird', 
    'chickadee', 'raven', 'wren', 'mallard', 'duck', 'bat',
    'pelican', 'swan', 'crane', 'stork', 'parrot', 'goose',
    'penguin', 'falcon', 'flamingo', 'peacock', 'puffin',
    'toucan', 'quail',
    'horse', 'sheep', 'pig', 'chicken', 'goat', 'cow', 
    'rooster', 'turkey', 'bull', 'donkey', 'mouse', 
    'lizard', 'frog', 'toad', 'gecko', 'iguana',
    'monkey', 'baboon', 'bandicoot', 'sloth', 'armadillo',
    'dolphin', 'whale', 'seahorse', 'octopus', 'squid', 'crab',
    'snail', 'bee', 'dragonfly', 'cricket', 'firefly',
    'butterfly', 'moth', 'salamander',
    'llama', 'lemming', 'tortoise', 'reindeer', 'moose', 
    'kangaroo', 'koala', 'panda', 'wallaby', 'gorilla'
];

function getRandomSubarray(arr, size) {
    // A "Fisher-Yates shuffle"
    // From: http://stackoverflow.com/questions/11935175/sampling-a-random-subset-from-an-array/11935263
    var shuffled = arr.slice(0), i = arr.length, min = i - size, temp, index;
    while (i-- > min) {
        index = Math.floor((i + 1) * Math.random());
        temp = shuffled[index];
        shuffled[index] = shuffled[i];
        shuffled[i] = temp;
    }
    return shuffled.slice(min);
}