"""In this example, we train a small neural network on some dummy data using the
`HessianFree` optimizer with preconditioning. We also demonstrate how to access
the optimizer's state after training.
"""

import torch
from example_utils import get_small_nn_testproblem

from hessianfree.optimizer import HessianFree

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


if __name__ == "__main__":

    print(f"\nRunning example on DEVICE = {DEVICE}")

    torch.manual_seed(0)

    # Set up problem and optimizer
    model, _, loss_function = get_small_nn_testproblem(device=DEVICE)
    opt = HessianFree(model.parameters(), verbose=True)

    for step_idx in range(2):
        print(f"\n===== STEP {step_idx} =====")

        # Sample new dummy data, define `forward` function
        _, (inputs, targets), _ = get_small_nn_testproblem(device=DEVICE)

        def forward():
            outputs = model(inputs)
            loss = loss_function(outputs, targets)
            return loss, outputs

        # Optional: Use the diagonal of the empirical Fisher as preconditioner
        M_func = opt.get_preconditioner(
            model, loss_function, inputs, targets, reduction="mean"
        )

        opt.step(
            forward=forward,
            M_func=M_func,
            test_deterministic=True if step_idx == 0 else False,
        )

    # Print state of optimizer after training
    state_dict = opt.state_dict()["state"]
    state_dict.pop("x0")

    print("\nState...")
    for key, val in state_dict.items():
        print(f"  {key:15}: {val}")
