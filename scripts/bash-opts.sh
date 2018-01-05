#!/usr/bin/env bash
#
# bash-opts.sh
#
# Library of helper functions for processing Bash script arguments flexibly
#
# Can handle:
#   * script.sh -h (short flags)
#   * script.sh --help (long flags)
#   * script.sh -o value (short options with values)
#   * script.sh -o=value (short options with an equal value)
#   * script.sh --option value (long options with values)
#   * script.sh --option=value (long options with equal values)
#   * script.sh arg1 arg2 --flag arg3 --option=value arg4 (mixed arguments)
#
# To use:
# 
#    SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
#    source "$SCRIPT_DIR/bash-opts.sh"
#    source "$SCRIPT_DIR/bash-validators.sh"
#
#    PARAMS=`normalize_params "$@"`  # PARAMS is an internal variable used by flag and option parsers
#
#    parse_flag '-h|--help' HELP_WANTED
#
#    if [ "$HELP_WANTED" ]
#    then
#      echo "$HELP"
#      echo "$USAGE"
#      exit 0
#    fi
#
#    parse_flag '-f|--flag' FLAG_BOOL || exit 1
#    parse_option '-o|--option' OPTION_VALUE validate_string "Option value can not be an empty string." || exit 2
#
#    ARGS=(`get_args "$PARAMS"`)
#
#    SCRIPT_ARG1="${ARGS[0]}"
#    SCRIPT_ARG2="${ARGS[1]}"
#      
#
#-------------------------------------------------------------------------------
# Convert parameters into newline separated sections and apply other 
# normalizations.
#
# This way we can avoid problems with quote expansion when passing parameters
# around.
#
# USAGE:> PARAMS=`normalize_params "$@"`
#
function normalize_params()
{
    local PARAMS=''
    
    for PARAM in "$@"
    do
        # Split single character flags
        if [[ $PARAM =~ ^-([A-Za-z0-9]{2,})$ ]]
        then
            BLOB=${BASH_REMATCH[1]}
            for ((i=0; i<${#BLOB}; i++)); do
                PARAMS="${PARAMS}-${BLOB:$i:1}"$'\n'
            done
        # Split equal '=' assignments   
        elif [[ $PARAM =~ ^(--?[A-Za-z0-9_-]+)\=(.+)$ ]]
        then
            PARAMS="${PARAMS}${BASH_REMATCH[1]}"$'\n'
            PARAMS="${PARAMS}${BASH_REMATCH[2]}"$'\n'  
        else       
            PARAMS="${PARAMS}${PARAM}"$'\n'
        fi
    done
    
    echo "$PARAMS"
    return 0    
}

#-------------------------------------------------------------------------------
# Return whether or not parameters have a particular flag enabled.
#
# USAGE:> parse_flag $FLAG FOUND_REF
#
# Note: Needs [ PARAMS="$@" ] defined in the calling function.
#       The flag is removed from this variable.
#
function parse_flag()
{
    local FLAGS="$1"
    local FOUND="$2"
    
    local LOCAL_FOUND=''
    
    local ALT_PARAMS=''
    local IFS_ORIG="$IFS"
    
    IFS='|'
    read -ra FLAG_ARRAY <<< "$FLAGS"
    
    IFS=$'\n'        
    for PARAM in $PARAMS  # $PARAMS is not a local variable
    do 
        # echo "PARAM = $PARAM"
        for FLAG in "${FLAG_ARRAY[@]}"
        do
           if [ "$PARAM" = "$FLAG" ]
           then
               eval $FOUND="$PARAM" # Notify parent script that flag was found.
               LOCAL_FOUND='1'
               
               # echo "Flag $FLAG found."
               break
           fi
        done
        
        if [ ! "$LOCAL_FOUND" ]
        then
           ALT_PARAMS="${ALT_PARAMS}${PARAM}"$'\n'
           # echo "ALT_PARAMS = $ALT_PARAMS"  
        fi
        
        LOCAL_FOUND=''
    done
    
    PARAMS=$ALT_PARAMS  # Reassign to calling function params.
    IFS="$IFS_ORIG"
    return 0
}

#-------------------------------------------------------------------------------
# Return whether or not parameters have a particular option specified.
#
# USAGE:> parse_option $OPTION VALUE_REF $VALIDATOR_FUNC $ERROR_MSG
#
# Note: Needs [ PARAMS="$@" ] defined in the calling function.
#       The option and value are removed from this variable.
#
function parse_option()
{
    local OPTIONS="$1"
    local VALUE="$2"
    local VALIDATOR="$3"
    local ERROR_MSG="$4"
    
    if [ ! "$VALIDATOR" ]
    then
      VALIDATOR='validate_string' # Default option value is non empty string
    fi
    
    local ALT_PARAMS=''
    local IFS_ORIG="$IFS"
        
    local OPTION_FOUND=''
    local VALUE_FOUND=''
    local NEEDS_PROCESSING=''
    
    IFS='|'
    read -ra OPTION_ARRAY <<< "$OPTIONS"
    
    IFS=$'\n'
    for PARAM in $PARAMS  # $PARAMS is not a local variable
    do 
        #echo "PARAM = $PARAM"
        if [ "$NEEDS_PROCESSING" ]
        then
            #echo "OPTION FOUND - Retreiving Value"
            if [[ $PARAM =~ ^- ]]
            then
                ERROR_MSG=`echo "Parameter [ $OPTIONS ] (empty): $ERROR_MSG"`
                echo "$ERROR_MSG"
                            
                IFS="$IFS_ORIG"
                return 1  
            fi
            
            if [ "$VALIDATOR" ]
            then
                #echo "$VALIDATOR '$PARAM'"
                if ! $VALIDATOR "$PARAM"
                then
                    ERROR_MSG=`echo "Parameter [ $OPTIONS ] ($PARAM): $ERROR_MSG"`
                    echo "$ERROR_MSG"
                    return 1
                fi
            fi
            eval $VALUE="'$PARAM'" # Notify parent script that option was found.
            VALUE_FOUND='1'
            NEEDS_PROCESSING=''
            continue
        fi
            
        for OPTION in "${OPTION_ARRAY[@]}"
        do
            #echo "OPTION  = $OPTION"                            
            if [ "$PARAM" = "$OPTION" ]
            then
              #echo "OPTION FOUND - Setting Flag"
              OPTION_FOUND='1'               
                NEEDS_PROCESSING='1'
                break
            fi
        done
        
        if [ ! "$NEEDS_PROCESSING" ]
        then
            ALT_PARAMS="${ALT_PARAMS}${PARAM}"$'\n'
            #echo "ALT_PARAMS = $ALT_PARAMS"
        fi
    done
    
    # Check if we have a value.
    if [ "$OPTION_FOUND" -a ! "$VALUE_FOUND" ]
    then
        ERROR_MSG=`echo "Parameter [ $OPTIONS ] (empty): $ERROR_MSG"`
        echo "$ERROR_MSG"
                            
        IFS="$IFS_ORIG"
        return 1  
    fi
    
    PARAMS=$ALT_PARAMS  # Reassign to calling function params.
    IFS="$IFS_ORIG"
    return 0
}

#-------------------------------------------------------------------------------
# Returns all non dashed arguments from list of parameters.
#
# This should be run after all flags and options have been parsed.
#
# USAGE:> ARGS=(`get_args "$PARAMS"`)
#
function get_args()
{
    local ARGS=()
    local IFS_ORIG="$IFS"
    
    IFS=$'\n'
    for PARAM in $@
    do
        # No options allowed
        if [[ $PARAM =~ ^[^-] ]]
        then
          ARGS=("${ARGS[@]}" "$PARAM")
        fi
    done
     
    echo "${ARGS[*]}"
    IFS="$IFS_ORIG"
    return 0    
}