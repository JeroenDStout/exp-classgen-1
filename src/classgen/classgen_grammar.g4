grammar classgen_grammar;	
    
// ------------------------------
//      tokens
// ------------------------------

NEWLINE         : [\r\n]+    -> channel( HIDDEN );
WHITESPACE      : [ \n\t\r]+ -> channel( HIDDEN );

TOKEN_TRUE      : 'true'  ;
TOKEN_FALSE     : 'false' ;
TOKEN_T         : 'T'     ;
TOKEN_F         : 'F'     ;
TOKEN_CURL_LH   : '{'     ;
TOKEN_CURL_RH   : '}'     ;
TOKEN_SQUARE_LH : '['     ;
TOKEN_SQUARE_RH : ']'     ;
TOKEN_ARROW_LW  : '<-'    ;
TOKEN_ARROW_RW  : '->'    ;
TOKEN_ARROW_SYM : '<->'   ;
TOKEN_IPLMAP_LW : ':<'    ;
TOKEN_IPLMAP_RW : ':>'    ;
TOKEN_PLUS      : '+'     ;
TOKEN_MINUS     : '-'     ;
KEYWORD_ENUM    : 'enum'  ;
KEYWORD_AKA     : 'aka'   ;
KEYWORD_AS      : 'as'    ;

IDENTIFIER_LIKE_INTRINSIC_INT
    : ('i' | 'u') FRAG_DEC_NAT_NUMBER FRAG_NONDIGIT (FRAG_NONDIGIT | FRAG_DIGIT)*
    ;
    
INTRINSIC_SINT
    : 'i' FRAG_DEC_NAT_NUMBER
    ;
    
INTRINSIC_UINT
    : 'u' FRAG_DEC_NAT_NUMBER
    ;
    
IDENTIFIER
    : FRAG_NONDIGIT (FRAG_NONDIGIT | FRAG_DIGIT)*
    | IDENTIFIER_LIKE_INTRINSIC_INT
    ;
    
FRAG_DEC_NAT_NUMBER
    : FRAG_DIGIT+
    ;

FRAG_NONDIGIT        : [a-zA-Z_] ;
FRAG_DIGIT           : [0-9]     ;


// ------------------------------
//    prog
// ------------------------------

prog
    : translation_unit EOF
    ;

translation_unit
    : translation_element*
    ;

translation_element
    : enum_declaration
    ;

// ------------------------------
//    enum
// ------------------------------

enum_declaration
    : KEYWORD_ENUM identifier_flex TOKEN_CURL_LH enum_declaration_element* TOKEN_CURL_RH
    ;
    
enum_declaration_element
    : enum_declaration_token_list
    | mapping_implied_declaration
    ;
    
enum_declaration_token_list
    : TOKEN_SQUARE_LH enum_declaration_token_list_element* TOKEN_SQUARE_RH
    ;
    
enum_declaration_token_list_element
    : identifier_pure (mapping_implied_implementation_statement ','?)*
    ;
    
// ------------------------------
//      maps
// ------------------------------

mapping_implied_declaration
    : identifier_flex TOKEN_IPLMAP_RW mapping_mapped_to_type mapping_default_value?
    ;
    
mapping_implied_implementation_statement
    : identifier_pure TOKEN_IPLMAP_RW mapping_value
    ;

mapping_mapped_to_type
    : identifier_pure
    | intrinsic
    ;

mapping_default_value
    : TOKEN_CURL_LH mapping_value TOKEN_CURL_RH
    ;

mapping_value
    : constant
    | identifier_pure
    ;
    
// ------------------------------
//      identifiers
// ------------------------------
    
identifier_name
    : name=IDENTIFIER
    ;
    
identifier_pure
    : identifier_name
    ;
    
identifier_flex
    : identifier_name
    | identifier_with_alias
    ;
    
identifier_with_alias
    : name=IDENTIFIER KEYWORD_AKA identifier_alias_list
    ;
    
identifier_alias_list
    : IDENTIFIER (',' alias=IDENTIFIER)*
    ;
    
// ------------------------------
//      intrinsics
// ------------------------------

intrinsic
    : intrinsic_boolean
    | intrinsic_unsigned_integer
    | intrinsic_signed_integer
    ;
    
intrinsic_boolean
    : 'bool'
    ;

intrinsic_unsigned_integer
    : INTRINSIC_UINT
    ;
    
intrinsic_signed_integer
    : INTRINSIC_SINT
    ;
    
// ------------------------------
//      constants
// ------------------------------

constant
    : constant_boolean
    | constant_integer
    ;
    
constant_boolean
    : (constant_boolean_true | constant_boolean_false)
    ;
    
constant_boolean_true
    : (TOKEN_TRUE | TOKEN_T)
    ;
    
constant_boolean_false
    : (TOKEN_FALSE | TOKEN_F)
    ;
    
constant_integer
    : FRAG_DEC_NAT_NUMBER
    ;