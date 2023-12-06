<<<<<<< HEAD
import models.quantization
from constants import TRANSFORMER_URL

=======
from constants import TRANSFORMER_PATH
import models.quantization
>>>>>>> a8eaea6 (Docs)
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="rofi_semantic scripts",
        description="Execute various bits and pieces of this package"
    )

    sub_parsers = parser.add_subparsers(
        help="Different modes for the package",
        dest="command_name"
    )

    parser_quantize = sub_parsers.add_parser(
        'quantize',
        aliases=['q'],
        description='Quantize the model for better execution performance on CPU'
    )

    parser_quantize.add_argument(
        '--save_dir', '-s',
        default='models',
        type=str
    )

    parser_quantize.add_argument(
        '--model', '-m',
        default=TRANSFORMER_PATH,
        type=str
    )

    args = parser.parse_args()

    if args.command_name == 'quantize':
        models.quantization.quantize(args.save_dir, args.model)

