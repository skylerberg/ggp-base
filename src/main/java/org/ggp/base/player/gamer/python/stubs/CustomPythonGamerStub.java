package org.ggp.base.player.gamer.python.stubs;
import org.ggp.base.player.gamer.python.PythonGamer;

/**
 * SamplePythonGamerStub is a stub pointing to a version of @RandomGamer that
 * has been implemented in Python. This stub needs to exist so that the Python
 * code can interoperate with the rest of the Java framework (and applications
 * like Kiosk and PlayerPanel as a result).
 *
 * @author Skyler Berg
 */
public final class CustomPythonGamerStub extends PythonGamer
{
    @Override
    protected String getPythonGamerModule() { return "custom_gamer"; }
    @Override
    protected String getPythonGamerName() { return "CustomPythonGamer"; }
}
