#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, sys, logging, click , json
from pprint import pprint

__path = os.path.realpath(os.path.join(__file__,'..')) 
if __path not in sys.path:sys.path.append(__path)

from corsica import corsica_dpe,JaguarConfig
    
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help', '-?'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--ip','-i',type=click.STRING , help='tables.',default="127.0.0.1:23")
@click.pass_context
def config(ctx,ip):
    """Command line - 'config' command"""
    ctx.obj = dict()
    ctx.obj['gl'] = JaguarConfig(ip)

@config.command('post')
@click.option('--file','-f',type=click.File() , help='Json file.')
@click.option('--table','-t',type=click.STRING , help='tables.',default="")
@click.pass_context
def jaguar_post(ctx,file,table):
    """Post Configure."""
    jaguar = ctx.obj['gl']
    config = json.load(file)
    if table != "":
        config = {table : config}
    config = corsica_dpe.corsica_config_check(config)
    jaguar.jaguarRunConfig(config)

@config.command('get')
@click.option('--file','-f',type=click.File() , help='Json file.')
@click.option('--table','-t',type=click.STRING , help='tables.',default="")
@click.option('--index',type=click.STRING , help='tables index.',default="")
@click.pass_context
def jaguar_get(ctx,file,table,index):
    """Show something."""
    jaguar = ctx.obj['gl']
    config = json.load(file)
    config = corsica_dpe.corsica_config_check(config)
    jaguar.jaguarRunConfig(config)

@config.command('check')
@click.option('--file','-f',type=click.File() , help='Json tables.')
@click.option('--outfile','-o' , help='Json tables.')
@click.option('--split','-s' ,is_flag=True,  help='Json tables.',default=False)
@click.pass_context
def jaguar_check(ctx,file,outfile,split):
    """Show all fields."""
    config = json.load(file)
    config = corsica_dpe.corsica_config_check(config)
    if outfile == None:
        pprint(config)
    elif split:
        for t in config:
            click.echo("Output file : %s"%outfile)
            with open(outfile,"w") as f:
                json.dump(config,f)
    else :
        click.echo("Output file : %s"%outfile)
        with open(outfile,"w") as f:
            json.dump(config,f)

@config.command('show')
@click.option('--table','-t',type=click.STRING , help='tables.',default=None)
@click.option('--file','-f',type=click.File() , help='Json tables.',default=None)
@click.pass_context
def jaguar_show(ctx,table,file):
    """Show all fields."""
    info = corsica_dpe.table_template_get(table)
    if table == None:
        for t in info.keys():
            click.echo(t)
    elif info != None:
        pprint(corsica_dpe.default_json[table])
    else:
        click.echo("Unknow type")
    if file != None and info != None:
        with open(file,"w") as f:
            json.dump(info,f)

if __name__ == '__main__':
    config()

