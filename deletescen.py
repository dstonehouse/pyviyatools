#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# deletescen.py
# february 2018
#
# Pass in a decision flow ID and delete its scenarios
#
# Examples:
# 
# deletescen.py -f d42e1859-1aed-471f-897f-6046e978ad31 -n 50 -q
#
# Change History
#
#  07MAR2023 Crated
# based on deletefolderandcontents

#
# Copyright © 2023, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

# Import Python modules

import argparse, sys
from sharedfunctions import getfolderid, callrestapi

defaultnumitems=10
parser = argparse.ArgumentParser(description="Delete the scenarios for a decision")
parser.add_argument("-f","--flowid", help="Enter the decision flow ID.",required='True')
parser.add_argument("-l","--listonly", help="List only.", action='store_true')
parser.add_argument("-n","--numitems", help=f"number of items to list/delete - default = {defaultnumitems}", type=int, default=10)
parser.add_argument("-q","--quiet", help="Suppress the are you sure prompt.", action='store_true')
args = parser.parse_args()
quietmode=args.quiet
flowid=args.flowid
listonly=args.listonly
numitems=args.numitems


reqval=f"/scoreDefinitions/definitions?sortBy=name&filter=and(contains(objectDescriptor.uri,'/decisions/flows/{flowid}'),or(isNull(folderType),ne(folderType,'trashFolder')),eq(inputData.type,'Scenario'))&limit={numitems}"

reqtype='get'
allchildren=callrestapi(reqval,reqtype)
# print (allchildren)
if 'items' in allchildren:
    itemlist = allchildren['items']
    # print(itemlist)
    lenitem=len(itemlist)
    if listonly:
        item_print_limit = lenitem
    else:
        item_print_limit = min(25, numitems)
    for children in itemlist[:item_print_limit]:
        linklist = children['links']
        for linkval in linklist:
            if linkval['rel'] == 'delete':
                reqval=(linkval['uri'])
                reqtype=(linkval['method']).lower()		    		
                print(reqval)
    
    if len(itemlist) > item_print_limit:
        print(f"\n... Stopping at {item_print_limit} items...")

    if listonly:
        areyousure="N"
    elif quietmode:
        areyousure="Y"
    else:        
        areyousure=input("Are you sure you want to delete scenarios for this decision flow? (Y) ")
    
    if areyousure.upper() == 'Y':
        deletecount=0
        for children in itemlist:
            linklist = children['links']
            for linkval in linklist:
                if linkval['rel'] == 'delete':
                    reqval=(linkval['uri'])
                    reqtype=(linkval['method']).lower()		    		
                    # print (f"deleting one: {reqval}")
                    callrestapi(reqval,reqtype) 
                    deletecount +=1
        print(f"Number deleted = {deletecount}")
else:
    print("Flow doesnt exist, or no scenarios for this flow")