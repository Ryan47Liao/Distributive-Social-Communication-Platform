# @title A4 {display-mode: "form"}
import nacl
import nacl.utils
from Profile import *
import copy
from nacl.public import PrivateKey, PublicKey, Box
from API_handling import *


# from Profile import *
def hex_to_EM(HEX_STR) -> nacl.utils.EncryptedMessage:
    try:
        bts = nacl.utils.encoding.HexEncoder.decode(HEX_STR)
    except:
        print("ERROR!Hex:failed to convert:", HEX_STR)
    return nacl.utils.EncryptedMessage(bts)


def EM_to_hex(encrypted_message: nacl.utils.EncryptedMessage) -> str:
    return encrypted_message.hex()


def encode_public_key(public_key: str) -> PublicKey:
    """
    encode_public_key takes an public_key string as a parameter and generates
    a PublicKey object.
    """

    return PublicKey(public_key, nacl.encoding.Base64Encoder)


def encode_private_key(private_key: str) -> PrivateKey:
    """
    encode_private_key takes an private_key string as a parameter and generates
    a PrivateKey object.
    """
    return PrivateKey(private_key, nacl.encoding.Base64Encoder)


class NaClProfile(Profile):
    def __init__(self, dsuserver="ws://168.235.86.101:9997/ws", username=None, password=None):
        self.dsupk = "G4eg7stY7kIJj7dYUFunrU9nSozh49vnkDlYSqHynwQ="
        self.dsuserver = dsuserver  # REQUIRED
        self.bio = ''  # OPTIONAL
        self.__posts = []  # OPTIONAL
        # Fetch Keys:
        self.keypair = self.generate_keypair()
        self.import_keypair(self.keypair)
        
    def get_public_key(self, pk):
        self.dsupk = pk

    def generate_keypair(self) -> str:
        """
        Use the NaClDSEncoder module to generate a new keypair and populate
        the public data attributes created in the initializer.

        returns keypair:str
        """
        # Creating NEW Pair of Keys:
        raw = PrivateKey.generate()
        private_key = raw.encode(encoder=nacl.encoding.Base64Encoder).decode(encoding='UTF-8')
        public_key = raw.public_key.encode(encoder=nacl.encoding.Base64Encoder).decode(encoding='UTF-8')
        keypair = private_key + "$" + public_key
        return keypair

    def import_keypair(self, keypair: str):
        """
        This method should use the keypair parameter to populate the public data attributes created by
        the initializer.
        """
        self.password = keypair[0:44] # private_key
        self.username = keypair[44:len(keypair)]  # public_key
        pass

    def add_post(self, post: Post) -> None:
        """

        add_post accepts a Post object as parameter and appends it to the posts list.
        Posts are stored in a list object in the order they are added. So if multiple Posts objects are created,
        but added to the Profile in a different order, it is possible for the list to not be sorted by the Post.timestamp property.
        So take caution as to how you implement your add_post code.

        [New]:Before a post is added to the profile, it should be encrypted. Remember to take advantage of the
        code that is already written in the parent class.
        """
        # Step 1 Encript the Message Based on Your Private Key and DSU Public Key
        original_message = post.entry
        encrypted_message = self.encrypt_entry(original_message, self.dsupk)
        post_enc = copy.deepcopy(post)
        post_enc.setpost(encrypted_message)
        # Step 2: add the modified post to the list
        self.__posts.append(post_enc)

        # print(self.__posts)
        
    def replace_post(self,idx,post):
        "Delete a post based on the entry"
        original_message = post.entry
        encrypted_message = self.encrypt_entry(original_message, self.dsupk)
        post_enc = copy.deepcopy(post)
        post_enc.setpost(encrypted_message)
        self.__posts[idx] = post_enc
        #encrypted_message = self.encrypt_entry(entry, self.dsupk)
        #for post in self.__posts:
            #if post.entry == encrypted_message:
                #self.__posts.remove(post)

    def Decript(self,HEX,password,dsupk = "jIqYIh2EDibk84rTp0yJcghTPxMWjtrt5NW4yPZk3Cw="):
        try:
            sk = encode_private_key(password)
            pk = encode_public_key(dsupk)
            box = Box(sk, pk)
            EM = hex_to_EM(HEX)
            plaintext = box.decrypt(EM).decode('utf-8')
        except:
            plaintext = '__ERROR__'

        return plaintext
    
    def get_posts(self) -> list:
        """

        get_posts returns the list object containing all posts that have been added to the Profile object

        """
        list_of_posts_enc = copy.deepcopy(self._NaClProfile__posts)
        list_of_posts_plain = []
        for post_enc in list_of_posts_enc:
            HEX = post_enc.entry
            plaintext = self.Decript(HEX,self.password,self.dsupk)
            post_enc.setpost(plaintext)
            list_of_posts_plain.append(post_enc)

        return list_of_posts_plain


    def encrypt_entry(self, entry: str, public_key: str) -> str:
        entry = entry.encode('utf-8')
        sk = encode_private_key(self.password)
        pk = encode_public_key(public_key)
        box = Box(sk, pk)
        encrypted = box.encrypt(entry)
        """
        This method will be used to encrypt messages using a 3rd party public key, such as the one that
        the DS server provides.

        returns encrypted_message:bytes 
        """
        return EM_to_hex(encrypted)

    def load_profile(self, path: str) -> None:
        "Rewrite the Profile Load..."
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsupk = obj['dsupk']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                try:
                    for post_obj in obj['__posts']:
                        post = Post(post_obj['entry'])
                        post.timestamp = post_obj['timestamp']
                        self.__posts.append(post)
                    f.close()
                except KeyError:
                    for post_obj in obj['_NaClProfile__posts']:
                        post = Post(post_obj['entry'])
                        post.timestamp = post_obj['timestamp']
                        self._NaClProfile__posts.append(post)
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()


def get_pk(json_str) -> str:
    DIC = json_to_dict(json_str)
    for key in DIC:
        if 'public_key' in key:
            return DIC[key]
    return "G4eg7stY7kIJj7dYUFunrU9nSozh49vnkDlYSqHynwQ="


if __name__ == '__main__':
    # Perform a Test
    NP = NaClProfile()
    kp = NP.generate_keypair()
    print(NP.username)
    print(NP.password)
    print(NP.keypair)

    ds_pubkey = "G4eg7stY7kIJj7dYUFunrU9nSozh49vnkDlYSqHynwQ="
    ee = NP.encrypt_entry("Encrypted Message for DS Server", ds_pubkey)
    print(ee)
    print(type(ee))

    print('\nAdd a post to the profile and check that it is decrypted.')
    NP.add_post(Post("Hello Salted World!"))
    NP.add_post(Post("YOOOOOOOOO!"))
    p_list = NP.get_posts()

    print("\nPlain Test:")
    print(p_list)

    print('\n access directly:')
    print(NP._NaClProfile__posts)
