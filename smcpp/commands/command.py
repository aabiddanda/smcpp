# Base class; subclasses will automatically show up as subcommands
import argparse

from ..logging import setup_logging


class Command:
    def __init__(self, parser):
        parser.add_argument('-v', '--verbose', action='count', default=0,
                help="increase debugging output, specify multiply times for more")

    def main(self, args):
        setup_logging(args.verbose)


def add_common_estimation_args(parser):
    parser.add_argument("-o", "--outdir", help="output directory", default=".")
    data = parser.add_argument_group('data parameters')
    data.add_argument('--nonseg-cutoff', '-c',
                      help="recode nonsegregating spans > cutoff as missing. "
                      "default: do not recode.",
                      type=int)
    data.add_argument('--length-cutoff',
                      help="omit sequences < cutoff. default: 10000", default=10000, type=int)
    data.add_argument('--thinning', help="only emit full SFS every <k>th site. default: 500 * n.",
                      default=None, type=int, metavar="k")
    data.add_argument('--no-filter', help="do not drop contigs with extreme heterozygosity. "
                                          "(not recommended unless data set is small)",
                      action="store_true", default=False)

    optimizer = parser.add_argument_group("Optimization parameters")
    optimizer.add_argument(
        "--no-initialize", action="store_true", default=False, help=argparse.SUPPRESS)
    optimizer.add_argument('--em-iterations', type=int,
                           help="number of EM steps to perform", default=10)
    optimizer.add_argument('--algorithm', choices=["L-BFGS-B", "TNC"],
                           default="L-BFGS-B", help=argparse.SUPPRESS)
    optimizer.add_argument('--blocks', type=int, 
                           help="number of coordinate ascent blocks")
    optimizer.add_argument('--factr', type=float,
                           default=1e-9, help=argparse.SUPPRESS)
    optimizer.add_argument('--regularization-penalty',
                           type=float, help="regularization penalty", default=1.)
    optimizer.add_argument("--tolerance", type=float, default=1e-4,
                           help="stopping criterion for relative improvement in loglik "
                           "in EM algorithm")
    optimizer.add_argument('--Nmin', type=float,
                           help="Lower bound on effective population size (in units of N0)",
                           default=.01)
    add_hmm_args(parser)

def add_hmm_args(parser):
    hmm = parser.add_argument_group("HMM parameters")
    hmm.add_argument(
        '--M', type=int, help="number of hidden states", default=32)

    polarization = parser.add_mutually_exclusive_group(required=False)
    polarization.add_argument("--fold", action="store_true", default=False,
                              help="use folded SFS (alias for -p 0.5)")
    polarization.add_argument('--polarization-error', '-p',
                              metavar='p', type=float, default=0.,
                              help="uncertainty parameter for polarized SFS: observation (a,b) "
                              "has probability [(1-p)*CSFS_{a,b} + p*CSFS_{2-a,n-2-b}]. "
                              "default: 0.0")
