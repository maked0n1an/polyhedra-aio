from enum import Enum


class Activity(Enum):
    GREENFIELD_TESTNET_MINT                 = 1     # Mint a Greenfield Testnet Tutorial NFT at https://zkbridge.com/nft-gfd
                                                    # and retweet https://twitter.com/PolyhedraZK/status/1665665972370550785
    OP_BNB_MINT_OPERATIONS                  = 2     # (Mint a opBNB NFT on zkbridge) and (Transfer your opBNB NFT to opBNB Chain)
    PANDRA_CODECONQUEROR_OPERATIONS         = 3     # Mint and bridge a “CodeConqueror” NFT from BNB to Polygon, Combo, Core DAO or Celo.
    PANDRA_PIXELBROWLER_OPERATIONS          = 4     # Mint and bridge a “PixelProwler” NFT from Polygon to BNB, Combo, Core DAO or Celo.
    PANDRA_MELODYMAVEN_OPERATIONS           = 5     # Mint and bridge a “MelodyMaven” NFT from Core DAO to BNB, Polygon or Combo.
    PANDRA_ECOGUARDIAN_OPERATIONS           = 6     # Mint and bridge a “EcoGuardian” NFT from Celo to BNB, Polygon or Combo.
    MAINNET_ALPHA_NFT_CORE_DAO_OPERATIONS   = 7     # Mint and bridge
    BSC_POLYGON_ZKMESSENGER                 = 8     # Send a cross-chain message using Greenfield zkMessenger on https://zkbridge.com/messenger before August 1st, 2023.
    ZK_LIGHT_CLIENT_NFT_OPERATIONS          = 9     # Mint and bridge